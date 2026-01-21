# ETA Calculation Algorithms

OctoPrint-TempETA implements two algorithms for estimating time to target temperature.

## Linear Algorithm

The default algorithm assumes a constant heating/cooling rate.

### Theory

For heating/cooling with approximately constant power:

```
rate = ΔT / Δt  (°C per second)
ETA = (T_target - T_current) / rate
```

### Implementation

```python
def calculate_linear_eta(self, history, target):
    """
    Calculate ETA using linear extrapolation.

    Args:
        history: deque of (timestamp, temperature, target) tuples
        target: Target temperature

    Returns:
        Estimated seconds to target, or None if insufficient data
    """
    if len(history) < 2:
        return None

    # Use last 10 seconds of data
    now = time.time()
    recent = [h for h in history if h[0] > now - 10]

    if len(recent) < 2:
        return None

    # Calculate rate: ΔT / Δt
    t0, temp0, _ = recent[0]
    t1, temp1, _ = recent[-1]

    delta_t = t1 - t0
    delta_temp = temp1 - temp0

    if delta_t <= 0:
        return None

    rate = delta_temp / delta_t  # °C/s

    # Check minimum rate threshold
    if abs(rate) < self.min_rate:
        return None

    # Calculate remaining temperature difference
    remaining = target - temp1

    # Same sign = approaching target
    # Different sign = moving away
    if (remaining > 0 and rate > 0) or (remaining < 0 and rate < 0):
        eta = abs(remaining / rate)
        return min(eta, self.max_eta)

    return None
```

### Advantages

- **Simple**: Easy to understand and debug
- **Fast**: Minimal computation
- **Robust**: Works well for most heating scenarios

### Limitations

- **Inaccurate for thermal lag**: Doesn't account for heat dissipation
- **Poor near target**: Rate changes as temperature stabilizes
- **Overshoot issues**: Can't predict thermal overshoot

### Best Use Cases

- Initial heating phase (far from target)
- Constant power heating
- When speed is more important than accuracy

## Exponential Algorithm

Models thermal dynamics using first-order exponential decay/growth.

### Theory

Temperature change follows Newton's Law of Cooling:

```
T(t) = T_ambient + (T_initial - T_ambient) * e^(-t/tau)
```

For heating to target with thermal losses:

```
T(t) = T_target - (T_target - T_0) * e^(-t/tau)
```

Where `tau` is the thermal time constant.

### Implementation

```python
def calculate_exponential_eta(self, history, target):
    """
    Calculate ETA using exponential model.

    Args:
        history: deque of (timestamp, temperature, target) tuples
        target: Target temperature

    Returns:
        Estimated seconds to target, or None if insufficient data
    """
    if len(history) < 3:
        return None

    # Use last 30 seconds for fitting
    now = time.time()
    recent = [h for h in history if h[0] > now - 30]

    if len(recent) < 3:
        return None

    # Extract time and temperature arrays
    times = np.array([h[0] for h in recent])
    temps = np.array([h[1] for h in recent])

    # Normalize time to start at 0
    times = times - times[0]
    current_temp = temps[-1]

    # Fit exponential model: T(t) = T_f - (T_f - T_0) * e^(-t/tau)
    try:
        # Use scipy.optimize.curve_fit or manual least-squares
        tau = self._fit_time_constant(times, temps, target)

        if tau <= 0 or tau > self.max_tau:
            return None

        # Calculate ETA: solve for t when T(t) = target
        # t = -tau * ln((target - T_f) / (current - T_f))

        remaining = target - current_temp
        initial_diff = temps[0] - target

        if abs(remaining) < 0.5:  # Close enough
            return 0

        ratio = remaining / initial_diff

        if ratio <= 0 or ratio >= 1:
            return None

        eta = -tau * math.log(ratio)
        return min(max(eta, 0), self.max_eta)

    except (ValueError, RuntimeError, FloatingPointError):
        # Fitting failed, fall back to None
        return None
```

### Time Constant Fitting

```python
def _fit_time_constant(self, times, temps, target):
    """
    Fit exponential time constant from temperature data.

    Uses linear regression on log-transformed data:
    ln(T - T_target) = ln(T_0 - T_target) - t/tau
    """
    # Transform to linear: y = ln|T - T_target|
    diff = temps - target

    # Avoid log(0) or log(negative)
    if np.any(np.abs(diff) < 0.1):
        raise ValueError("Too close to target for fitting")

    y = np.log(np.abs(diff))

    # Linear regression: y = a + b*t, where b = -1/tau
    A = np.vstack([times, np.ones(len(times))]).T
    b, a = np.linalg.lstsq(A, y, rcond=None)[0]

    if b >= 0:
        raise ValueError("Positive slope indicates moving away")

    tau = -1 / b
    return tau
```

### Advantages

- **Accurate**: Models real thermal behavior
- **Better near target**: Accounts for decreasing rate
- **Predictive**: Can forecast overshoot

### Limitations

- **Complex**: More computation required
- **Needs data**: Requires 30+ seconds of history
- **Fitting errors**: Can fail with noisy data

### Best Use Cases

- Final approach to target temperature
- High-precision requirements
- When thermal modeling is important

## Algorithm Selection

The plugin allows users to choose:

```yaml
plugins:
  temp_eta:
    algorithm: "linear"  # or "exponential"
```

### Recommendation

- **Linear**: Default, works well for most users
- **Exponential**: Advanced users, precision heating

## Hybrid Approach (Future)

A potential improvement is to use both algorithms:

```python
def calculate_hybrid_eta(self, history, target):
    """Use linear far from target, exponential when close."""
    current = history[-1][1]
    diff = abs(target - current)

    if diff > 20:  # Far from target
        return self.calculate_linear_eta(history, target)
    else:  # Close to target
        return self.calculate_exponential_eta(history, target)
```

## Edge Cases

### Cooling

Both algorithms work for cooling (negative rate):

```python
rate = delta_temp / delta_t  # Negative for cooling
remaining = target - current  # Negative when cooling
```

### Target Changes

When target changes during heating:

```python
def _on_target_changed(self, heater, new_target):
    # Clear history to avoid using data from old target
    self._history[heater].clear()
```

### Stalled Heating

If rate drops below threshold:

```python
if abs(rate) < self.min_rate:
    return None  # "Stalled" - no ETA
```

### Overshoot

Temperature overshooting target:

```python
if (current > target and rate > 0) or (current < target and rate < 0):
    return 0  # Already at/past target
```

## Performance

### Linear Algorithm

- **Time**: O(1) - processes last 2 samples
- **Memory**: O(1) - no additional storage
- **Latency**: < 1ms

### Exponential Algorithm

- **Time**: O(n) - processes up to 30 samples
- **Memory**: O(n) - temporary arrays
- **Latency**: < 10ms (with numpy)

## Testing

Both algorithms have comprehensive tests:

```python
def test_linear_heating():
    """Test linear algorithm with constant heating rate."""
    history = deque()
    for i in range(10):
        history.append((i, 25 + i * 2, 200))

    calc = Calculator(algorithm="linear")
    eta = calc.calculate_eta(history, 200)

    # Rate = 2°C/s, remaining = 175°C
    # Expected ETA = 175 / 2 = 87.5s
    assert abs(eta - 87.5) < 0.1
```

See [Testing](../development/testing.md) for more examples.

## Configuration

Algorithm-specific settings:

```yaml
plugins:
  temp_eta:
    algorithm: "linear"
    min_rate: 0.1          # Minimum rate (°C/s) to show ETA
    max_eta: 3600          # Maximum ETA (seconds)
    history_window: 10     # Seconds of history for linear
    fitting_window: 30     # Seconds for exponential fitting
```

## References

- [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) - Original request
- Newton's Law of Cooling - [Wikipedia](https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling)
- Thermal Time Constant - [Engineering](https://www.engineeringtoolbox.com/thermal-time-constant-d_1006.html)

## Next Steps

- [Python API](../api/python.md) - Implementation details
- [Settings](settings.md) - Configuration reference
- [Testing](../development/testing.md) - Algorithm tests
