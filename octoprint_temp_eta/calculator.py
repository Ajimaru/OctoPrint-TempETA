"""
Temperature ETA calculation algorithms.

This module provides pure calculation logic for estimating time remaining
until a printer heater reaches its target temperature or cools down.

All functions are stateless and independent of OctoPrint plugin mechanics,
making them easy to test and maintain.
"""

import logging
import math
from collections import deque
from typing import Optional

_LOG = logging.getLogger("octoprint_temp_eta")

# Smallest assumed gap between the target and the heater's steady state, used
# when scanning candidate asymptotes for the exponential fit.
ASYMPTOTE_MIN_MARGIN_C = 1.0

# Sanity bounds for an exponential estimate measured against the linear one.
# The previous guard only rejected estimates above 5x linear, which was loose
# enough that bad values simply pinned just under the limit instead of being
# caught. Divergence beyond this ratio, once it also exceeds the absolute
# slack, means the fit is not describing the observed heating.
EXP_SANITY_MAX_RATIO = 2.0
EXP_SANITY_SLACK_S = 20.0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_last_ts(pairs) -> Optional[float]:
    """Return the largest finite timestamp from an iterable of (ts, temp, ...) rows."""
    last = None
    for row in pairs:
        ts = row[0]
        temp = row[1]
        if math.isfinite(ts) and math.isfinite(temp):
            last = ts if (last is None or ts > last) else last
    return last


def _filter_recent(pairs, cutoff: float):
    """Return rows from *pairs* with ts > cutoff and finite ts/temp, sorted by ts."""
    return sorted(
        (
            row
            for row in pairs
            if row[0] > cutoff and math.isfinite(row[0]) and math.isfinite(row[1])
        ),
        key=lambda x: x[0],
    )


def _dedupe_by_ts(rows):
    """Remove consecutive duplicate timestamps."""
    out = []
    prev = None
    for row in rows:
        if prev is not None and row[0] == prev:
            continue
        out.append(row)
        prev = row[0]
    return out


def _linear_regression(xs, ys):
    """Return (slope, intercept) from lists xs/ys, or None if degenerate."""
    n = len(xs)
    if n < 2:
        return None
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    sxx = sum((x - x_mean) ** 2 for x in xs)
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    if sxx <= 0:
        return None
    slope = sxy / sxx
    return slope, y_mean - slope * x_mean


def _smoothed_last_temp(recent) -> float:
    """
    Current temperature as the median of the last few samples.

    A single spurious reading at the end of the window would otherwise shift
    the remaining distance and visibly jump the countdown. The median of three
    rejects such a spike while still tracking a genuine stall or dip.
    """
    # Only smooth with a full three samples: with two, the median of an even
    # tail returns the upper value, which on a monotonic ramp is the stale
    # older reading rather than the current temperature.
    if len(recent) < 3:
        return recent[-1][1]
    return sorted(row[1] for row in recent[-3:])[1]


def _validate_scalar(value: float) -> bool:
    return math.isfinite(value)


def _validate_window(window_seconds: float) -> bool:
    return math.isfinite(window_seconds) and window_seconds > 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def calculate_linear_eta(
    history: deque, target: float, window_seconds: float = 10.0
) -> Optional[float]:
    """
    Calculate ETA assuming constant heating rate.

    Estimates the heating rate by least-squares regression over all samples
    within the recent time window and extrapolates linearly to the target.

    Args:
        history: Deque of (timestamp, actual_temp, target_temp) tuples
        target: Target temperature in degrees
        window_seconds: Time window for rate calculation (default: 10s)

    Returns:
        Estimated seconds to target, or None if insufficient data
        or the heater is not heating within the window
    """
    if not _validate_scalar(target) or not _validate_window(window_seconds):
        return None
    if not history or len(history) < 2:
        return None

    last_ts = _find_last_ts(history)
    if last_ts is None:
        return None

    recent = _filter_recent(history, last_ts - window_seconds)
    if len(recent) < 2:
        return None

    t0 = recent[0][0]
    temp_now = _smoothed_last_temp(recent)

    # Least-squares slope over the whole window rather than just the first and
    # last sample: a single noisy reading (or a PID overshoot dip) would
    # otherwise swing the rate and make the countdown jump between updates.
    fit = _linear_regression(
        [row[0] - t0 for row in recent], [row[1] for row in recent]
    )
    if fit is None:
        return None

    rate = fit[0]
    if rate <= 0:
        return None

    remaining = target - temp_now
    if remaining <= 0:
        return None

    return max(0.0, remaining / rate)


def _fit_asymptote(recent, target: float):
    """
    Estimate the heater's steady-state temperature from *recent* samples.

    A heater driven to *target* does not asymptote at *target*: the controller
    overshoots, so the true asymptote sits above it. Fitting log(target - temp)
    therefore inflates tau as the temperature closes in on the target, which in
    turn inflates the ETA. Scan a few plausible margins above target and keep
    the fit whose reconstructed temperatures best match the original samples.

    Returns (asymptote, slope), or None when nothing fits.
    """
    t0 = recent[0][0]
    xs_all = [row[0] - t0 for row in recent]
    temps = [row[1] for row in recent]

    best = None
    for margin_frac in (0.0, 0.02, 0.05, 0.10, 0.20):
        asymptote = target + max(ASYMPTOTE_MIN_MARGIN_C, target * margin_frac)
        xs = []
        ys = []
        retained_temps = []
        for x, temp in zip(xs_all, temps):
            delta = asymptote - temp
            if delta <= 0 or x < 0:
                continue
            xs.append(x)
            ys.append(math.log(delta))
            retained_temps.append(temp)
        if len(xs) < 6:
            continue
        result = _linear_regression(xs, ys)
        if result is None:
            continue
        slope, intercept = result
        if slope >= -1e-4:
            continue
        # Compare errors in temperature space: log-space errors shrink as the
        # candidate asymptote increases, biasing selection toward larger margins.
        rss = sum(
            (temp - (asymptote - math.exp(slope * x + intercept))) ** 2
            for x, temp in zip(xs, retained_temps)
        )
        if best is None or rss < best[0]:
            best = (rss, asymptote, slope)

    if best is None:
        return None
    return best[1], best[2]


def _exponential_fit(recent, target: float):
    """
    Fit an exponential heating model to *recent* samples.

    Returns estimated eta in seconds, or None to signal fallback to linear.
    May propagate exceptions from math.log (e.g. ValueError) to the caller.
    """
    xs_span = recent[-1][0] - recent[0][0]
    if len(recent) < 6 or xs_span < 5:
        return None  # not enough span → fallback

    if (recent[-1][1] - recent[0][1]) <= 0.2:
        return None  # not heating → fallback

    fit = _fit_asymptote(recent, target)
    if fit is None:
        return None  # no plausible asymptote → fallback

    asymptote, slope = fit

    tau = -1.0 / slope
    if tau > 2000:
        return None  # implausibly slow time constant → fallback

    temp_now = recent[-1][1]
    remaining_now = asymptote - temp_now
    remaining_at_target = asymptote - target
    if remaining_now <= 0 or remaining_at_target <= 0:
        return None

    # Time for (asymptote - T) to decay from its current value to the value it
    # holds when T reaches the target. Referencing the target this way means the
    # ETA no longer depends on closing to within epsilon of the asymptote.
    # ValueError propagates to calculate_exponential_eta for fallback handling
    eta = tau * math.log(remaining_now / remaining_at_target)
    return max(0.0, eta)


def calculate_exponential_eta(
    history: deque, target: float, window_seconds: float = 30.0
) -> Optional[float]:
    """
    Calculate ETA accounting for thermal asymptotic behavior.

    Uses exponential model: T(t) = T_final - (T_final - T_0) * e^(-t/tau)
    Falls back to linear estimation when insufficient data or poor fit.

    Args:
        history: Deque of (timestamp, actual_temp, target_temp) tuples
        target: Target temperature in degrees
        window_seconds: Time window for exponential fit (default: 30s)

    Returns:
        Estimated seconds to target, or None if insufficient data
    """
    if not _validate_scalar(target) or not _validate_window(window_seconds):
        return None
    if not history or len(history) < 3:
        return None

    last_ts = _find_last_ts(history)
    if last_ts is None:
        return None

    recent = _dedupe_by_ts(_filter_recent(history, last_ts - window_seconds))
    if len(recent) < 6:
        return calculate_linear_eta(history, target)

    temp_now = recent[-1][1]
    remaining_now = target - temp_now
    if remaining_now <= 0:
        return None

    # Guard: window must show meaningful heating; otherwise no ETA is possible.
    if (recent[-1][1] - recent[0][1]) <= 0.2:
        return None

    epsilon_c = 0.5
    if remaining_now <= epsilon_c:
        return 0.0

    try:
        eta = _exponential_fit(recent, target)
    except (ValueError, ArithmeticError) as exc:
        _LOG.debug("Exponential ETA math error: %s", exc)
        return calculate_linear_eta(history, target)

    if eta is None:
        return calculate_linear_eta(history, target)

    linear_eta = calculate_linear_eta(history, target)
    if linear_eta is not None:
        # Absolute slack keeps short ETAs (where a few seconds is a large
        # ratio) from being rejected for no reason; the ratio catches the
        # sustained over-estimates that a ratio-only guard let through.
        if abs(eta - linear_eta) > EXP_SANITY_SLACK_S and (
            eta > linear_eta * EXP_SANITY_MAX_RATIO
            or eta * EXP_SANITY_MAX_RATIO < linear_eta
        ):
            _LOG.debug(
                "Exponential ETA %.1fs rejected against linear %.1fs", eta, linear_eta
            )
            return linear_eta

    return eta


def calculate_cooldown_linear_eta(
    cooldown_history: deque, goal_c: float, window_seconds: float = 60.0
) -> Optional[float]:
    """
    Linear cooldown ETA from recent slope.

    Estimates the cooling rate by least-squares regression over all samples
    within the recent time window and extrapolates linearly to the goal. The
    result is capped at 24 hours.

    Args:
        cooldown_history: Deque of (timestamp, temp) tuples
        goal_c: Target cooldown temperature in degrees
        window_seconds: Time window for fit (default: 60s)

    Returns:
        Estimated seconds to goal, or None if insufficient data
        or the heater is not cooling within the window
    """
    if not _validate_scalar(goal_c) or not _validate_window(window_seconds):
        return None
    if not cooldown_history:
        return None

    last_ts = _find_last_ts(cooldown_history)
    if last_ts is None:
        return None

    recent = _filter_recent(cooldown_history, last_ts - window_seconds)
    if len(recent) < 2:
        return None

    t0 = recent[0][0]
    temp_now = _smoothed_last_temp(recent)

    # Least-squares over the window, matching the heating path: a single noisy
    # reading should not swing the cooldown countdown between updates.
    fit = _linear_regression(
        [row[0] - t0 for row in recent], [row[1] for row in recent]
    )
    if fit is None:
        return None

    slope = fit[0]
    if slope >= -1e-3:
        return None

    remaining = temp_now - goal_c
    if remaining <= 0:
        return None

    eta = remaining / (-slope)
    if not math.isfinite(eta) or eta < 0:
        return None

    return float(min(eta, 24 * 3600))


def _cooldown_exponential_fit(recent, ambient_c: float, goal_c: float, epsilon: float):
    """
    Fit Newton's law of cooling to *recent* (ts, temp) samples.

    Returns eta in seconds, or None if the fit is degenerate.
    """
    t0 = recent[0][0]
    xs = []
    ys = []
    for ts, temp in recent:
        delta = temp - ambient_c
        if delta <= epsilon:
            continue
        x = ts - t0
        if x < 0:
            continue
        xs.append(x)
        ys.append(math.log(delta))

    if len(xs) < 4:
        return None

    result = _linear_regression(xs, ys)
    if result is None:
        return None

    slope, _ = result
    if slope >= -1e-4:
        return None

    tau = -1.0 / slope
    if tau <= 0 or tau > 20000:
        return None

    temp_now = recent[-1][1]
    numerator = temp_now - ambient_c
    denominator = goal_c - ambient_c
    if numerator <= 0 or denominator <= 0:
        return None

    eta = tau * math.log(numerator / denominator)
    if not math.isfinite(eta) or eta < 0:
        return None

    return float(min(eta, 24 * 3600))


def calculate_cooldown_exponential_eta(
    cooldown_history: deque,
    ambient_c: float,
    goal_c: float,
    window_seconds: float = 60.0,
) -> Optional[float]:
    """
    Exponential cooldown ETA (Newton's law of cooling).

    Models cooldown as: T(t) = T_ambient + (T_0 - T_ambient) * e^(-t/tau)
    """
    if not (_validate_scalar(ambient_c) and _validate_scalar(goal_c)):
        return None
    if not _validate_window(window_seconds):
        return None
    if goal_c <= ambient_c:
        return None
    if not cooldown_history or len(cooldown_history) < 4:
        return None

    last_ts = _find_last_ts(cooldown_history)
    if last_ts is None:
        return None

    recent = _filter_recent(cooldown_history, last_ts - window_seconds)
    if len(recent) < 6:
        return calculate_cooldown_linear_eta(cooldown_history, goal_c, window_seconds)

    if recent[-1][1] <= goal_c:
        return None

    try:
        return _cooldown_exponential_fit(recent, ambient_c, goal_c, epsilon=0.5)
    except (ValueError, ArithmeticError) as exc:
        _LOG.debug("Exponential ETA math error: %s", exc)
        return None
