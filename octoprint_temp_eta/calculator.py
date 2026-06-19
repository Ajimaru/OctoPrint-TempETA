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

    Uses linear regression on recent temperature samples to estimate
    the rate of temperature change and predict time to target.

    Args:
        history: Deque of (timestamp, actual_temp, target_temp) tuples
        target: Target temperature in degrees
        window_seconds: Time window for rate calculation (default: 10s)

    Returns:
        Estimated seconds to target, or None if insufficient data
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

    t0, temp0 = recent[0][0], recent[0][1]
    t1, temp1 = recent[-1][0], recent[-1][1]
    time_diff = t1 - t0
    temp_diff = temp1 - temp0
    if time_diff <= 0 or temp_diff <= 0:
        return None

    remaining = target - temp1
    if remaining <= 0:
        return None

    return max(0.0, remaining / (temp_diff / time_diff))


def _exponential_fit(recent, target: float, epsilon_c: float):
    """
    Fit an exponential heating model to *recent* samples.

    Returns estimated eta in seconds, or None to signal fallback to linear.
    May propagate exceptions from math.log (e.g. ValueError) to the caller.
    """
    t0 = recent[0][0]
    xs = []
    ys = []
    for ts, temp, *_ in recent:
        delta = target - temp
        if delta <= epsilon_c:
            continue
        x = ts - t0
        if x < 0:
            continue
        xs.append(x)
        ys.append(math.log(delta))

    if len(xs) < 6 or (xs[-1] - xs[0]) < 5:
        return None  # not enough span → fallback

    if (recent[-1][1] - recent[0][1]) <= 0.2:
        return None  # not heating → fallback

    result = _linear_regression(xs, ys)
    if result is None:
        return None

    slope, _ = result
    if slope >= -1e-4 or not (-1.0 / slope) > 0 or (-1.0 / slope) > 2000:
        return None

    tau = -1.0 / slope
    remaining_now = target - recent[-1][1]
    # ValueError propagates to calculate_exponential_eta for fallback handling
    eta = tau * math.log(remaining_now / epsilon_c)
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
        eta = _exponential_fit(recent, target, epsilon_c)
    except (ValueError, ArithmeticError) as exc:
        _LOG.debug("Exponential ETA math error: %s", exc)
        return calculate_linear_eta(history, target)

    if eta is None:
        return calculate_linear_eta(history, target)

    linear_eta = calculate_linear_eta(history, target)
    if linear_eta is not None and eta > linear_eta * 5:
        return linear_eta

    return eta


def calculate_cooldown_linear_eta(
    cooldown_history: deque, goal_c: float, window_seconds: float = 60.0
) -> Optional[float]:
    """
    Linear cooldown ETA from recent slope.

    Uses linear regression on recent cooldown samples to estimate
    the rate of temperature decrease and predict time to goal.

    Args:
        cooldown_history: Deque of (timestamp, temp) tuples
        goal_c: Target cooldown temperature in degrees
        window_seconds: Time window for fit (default: 60s)

    Returns:
        Estimated seconds to goal, or None if insufficient data
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

    t0, temp0 = recent[0]
    t1, temp1 = recent[-1]
    dt = t1 - t0
    if dt <= 0:
        return None

    slope = (temp1 - temp0) / dt
    if slope >= -1e-3:
        return None

    remaining = temp1 - goal_c
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
