# coding=utf-8
"""Temperature ETA calculation algorithms.

This module provides pure calculation logic for estimating time remaining
until a printer heater reaches its target temperature or cools down.

All functions are stateless and independent of OctoPrint plugin mechanics,
making them easy to test and maintain.
"""

from __future__ import absolute_import

import math
import time
from collections import deque
from typing import Optional


def calculate_linear_eta(
    history: deque, target: float, window_seconds: float = 10.0
) -> Optional[float]:
    """Calculate ETA assuming constant heating rate.

    Uses linear regression on recent temperature samples to estimate
    the rate of temperature change and predict time to target.

    Args:
        history: Deque of (timestamp, actual_temp, target_temp) tuples
        target: Target temperature in degrees
        window_seconds: Time window for rate calculation (default: 10s)

    Returns:
        Estimated seconds to target, or None if insufficient data
    """
    # Validate inputs
    if not math.isfinite(target):
        return None
    if not math.isfinite(window_seconds) or window_seconds <= 0:
        return None

    if not history or len(history) < 2:
        return None

    # Use last N seconds of data for rate calculation
    now = time.time()
    cutoff = now - window_seconds
    t0 = None
    temp0 = None
    t1 = None
    temp1 = None

    for ts, actual, _target in history:
        # Validate data from history
        if not (math.isfinite(ts) and math.isfinite(actual)):
            continue
        if ts <= cutoff:
            continue
        if t0 is None:
            t0 = ts
            temp0 = actual
        t1 = ts
        temp1 = actual

    if t0 is None or t1 is None or temp0 is None or temp1 is None:
        return None

    time_diff = t1 - t0
    temp_diff = temp1 - temp0
    if time_diff <= 0 or temp_diff <= 0:
        eta = remaining / rate
        # cap at 24 hours
        return float(min(max(0.0, eta), 24 * 3600))
    # rate = ΔT / Δt (°C per second)
    rate = temp_diff / time_diff
    remaining = target - temp1

    if remaining <= 0:
        return None

    eta = remaining / rate
    return max(0.0, eta)


def calculate_exponential_eta(
    history: deque, target: float, window_seconds: float = 30.0
) -> Optional[float]:
    """Calculate ETA accounting for thermal asymptotic behavior.

    Uses exponential model: T(t) = T_final - (T_final - T_0) * e^(-t/tau)
    Falls back to linear estimation when insufficient data or poor fit.

    Args:
        history: Deque of (timestamp, actual_temp, target_temp) tuples
        target: Target temperature in degrees
        window_seconds: Time window for exponential fit (default: 30s)

    Returns:
        Estimated seconds to target, or None if insufficient data
    """
    # Validate inputs
    if not math.isfinite(target):
        return None
    if not math.isfinite(window_seconds) or window_seconds <= 0:
        return None

    if not history or len(history) < 3:
        return None

    now = time.time()
    recent = [
        h
        for h in history
        if len(h) >= 2
        and math.isfinite(h[0])
        and math.isfinite(h[1])
        and h[0] > now - window_seconds
    ]

    if len(recent) < 6:
        return calculate_linear_eta(history, target)

    # Current sample
    t_now, temp_now, _ = recent[-1]
    if not (math.isfinite(t_now) and math.isfinite(temp_now)):
        return None
    remaining_now = target - temp_now
    remaining_now = target - temp_now
    if remaining_now <= 0:
        return None

    # We model the approach to target as asymptotic. Since reaching target exactly
    # would be infinite time, estimate the time until we are within epsilon.
    epsilon_c = 0.5
    if remaining_now <= epsilon_c:
        return 0.0

    # Build regression data for ln(target - T).
    # Exclude points too close to target (noise dominates) and invalid samples.
    t0 = recent[0][0]
    xs = []
    ys = []
    for ts, temp, _ in recent:
        delta = target - temp
        if delta <= epsilon_c:
            continue
        x = ts - t0
        if x < 0:
            continue
        xs.append(x)
        ys.append(math.log(delta))

    if len(xs) < 6:
        return calculate_linear_eta(history, target)

    span = xs[-1] - xs[0]
    if span < 5:
        return calculate_linear_eta(history, target)

    # Require we are actually heating in this window.
    if (recent[-1][1] - recent[0][1]) <= 0.2:
        return None

    # Linear regression: y = a + b*x, where b should be negative.
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    sxx = 0.0
    sxy = 0.0
    for x, y in zip(xs, ys):
        dx = x - x_mean
        dy = y - y_mean
        sxx += dx * dx
        sxy += dx * dy

    if sxx <= 0:
        return calculate_linear_eta(history, target)

    slope = sxy / sxx
    if slope >= -1e-4:
        # Not decaying fast enough or unstable -> fallback.
        return calculate_linear_eta(history, target)

    tau = -1.0 / slope
    if tau <= 0 or tau > 2000:
        return calculate_linear_eta(history, target)

    # ETA to reach epsilon band.
    try:
        eta = tau * math.log(remaining_now / epsilon_c)
    except ValueError:
        return calculate_linear_eta(history, target)

    if eta < 0:
        eta = 0.0

    # Protect against spikes: if exponential estimate is wildly larger than
    # the linear estimate on the same data, trust the linear estimate.
    linear_eta = calculate_linear_eta(history, target)
    if linear_eta is not None and eta > (linear_eta * 5):
        return linear_eta

    return eta


def calculate_cooldown_linear_eta(
    cooldown_history: deque, goal_c: float, window_seconds: float = 60.0
) -> Optional[float]:
    """Linear cooldown ETA from recent slope.

    Uses linear regression on recent cooldown samples to estimate
    the rate of temperature decrease and predict time to goal.

    Args:
        cooldown_history: Deque of (timestamp, temp) tuples
        goal_c: Target cooldown temperature in degrees
        window_seconds: Time window for fit (default: 60s)

    Returns:
        Estimated seconds to goal, or None if insufficient data
    """
    # Validate inputs
    if not math.isfinite(goal_c):
        return None
    if not math.isfinite(window_seconds) or window_seconds <= 0:
        return None

    if not cooldown_history or len(cooldown_history) < 2:
        return None

    now = time.time()
    recent = [
        (ts, temp)
        for ts, temp in cooldown_history
        if ts > now - window_seconds and math.isfinite(ts) and math.isfinite(temp)
    ]
    if len(recent) < 2:
        return None

    t0, temp0 = recent[0]
    t1, temp1 = recent[-1]
    dt = t1 - t0
    dtemp = temp1 - temp0
    if dt <= 0:
        return None

    slope = dtemp / dt
    if slope >= -1e-3:
        # Not cooling fast enough
        return None

    remaining = temp1 - goal_c
    if remaining <= 0:
        return None

    eta = remaining / (-slope)
    if not math.isfinite(eta) or eta < 0:
        return None

    # Cap at 24 hours
    return float(min(eta, 24 * 3600))


def calculate_cooldown_exponential_eta(
    cooldown_history: deque,
    ambient_c: float,
    goal_c: float,
    if len(recent) < 6:
        return calculate_cooldown_linear_eta(cooldown_history, goal_c, window_seconds)
    """Exponential cooldown ETA (Newton's law of cooling).

    Models cooldown as: T(t) = T_ambient + (T_0 - T_ambient) * e^(-t/tau)

    Args:
        cooldown_history: Deque of (timestamp, temp) tuples
        ambient_c: Ambient temperature in degrees
        goal_c: Target cooldown temperature in degrees
        window_seconds: Time window for exponential fit (default: 60s)

    Returns:
        Estimated seconds to goal, or None if insufficient data
    """
    # Validate inputs
    if not (math.isfinite(ambient_c) and math.isfinite(goal_c)):
        return None
    if not math.isfinite(window_seconds) or window_seconds <= 0:
        return None
    if goal_c <= ambient_c:
        return None

    x_mean = sum(xs) / len(xs)
y_mean = sum(ys) / len(ys)

    now = time.time()
    recent = [
        (ts, temp)
        for ts, temp in cooldown_history
        if ts > now - window_seconds and math.isfinite(ts) and math.isfinite(temp)
    ]
    if len(recent) < 6:
        return None

    _t_now, temp_now = recent[-1]
    if temp_now <= goal_c:
        return None

    epsilon = 0.5
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

    x_mean = sum(xs) / float(len(xs))
    y_mean = sum(ys) / float(len(ys))
    sxx = 0.0
    sxy = 0.0
    for x, y in zip(xs, ys):
        dx = x - x_mean
        dy = y - y_mean
        sxx += dx * dx
        sxy += dx * dy

    if sxx <= 0:
        return None

    slope = sxy / sxx
    if slope >= -1e-4:
        return None

    tau = -1.0 / slope
    if tau <= 0 or tau > 20000:
        return None

    # Calculate ETA with specific error handling for math domain errors
    numerator = temp_now - ambient_c
    denominator = goal_c - ambient_c

    # Validate division operands to avoid domain errors
    if numerator <= 0 or denominator <= 0:
        return None

    try:
        eta = tau * math.log(numerator / denominator)
    except (ValueError, ZeroDivisionError):
        # ValueError: math domain error (log of negative or zero)
        # ZeroDivisionError: division by zero
        return None

    if not math.isfinite(eta) or eta < 0:
        return None

    # Cap at 24 hours
    return float(min(eta, 24 * 3600))
