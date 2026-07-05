# ETA Calculation Algorithms

All ETA math lives in [`octoprint_temp_eta/calculator.py`](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/octoprint_temp_eta/calculator.py)
as stateless module-level functions. The plugin class only selects the
algorithm, feeds it the per-heater history and broadcasts the result — see
[Data flow](data-flow.md).

There are four estimators:

| Function                             | Direction | Model                          | Default window |
| ------------------------------------ | --------- | ------------------------------ | -------------- |
| `calculate_linear_eta`               | Heating   | Constant rate (endpoint slope) | 10 s           |
| `calculate_exponential_eta`          | Heating   | First-order exponential        | 30 s           |
| `calculate_cooldown_linear_eta`      | Cooling   | Constant rate (endpoint slope) | 60 s           |
| `calculate_cooldown_exponential_eta` | Cooling   | Newton's law of cooling        | 60 s           |

All functions return the estimated seconds to target, or `None` when no
trustworthy estimate is possible. The plugin hides ETAs below one second, so
"almost there" never flickers a `0:00` countdown.

Heating history samples are `(timestamp, actual_temp, target_temp)` tuples;
cooldown history samples are `(timestamp, actual_temp)` tuples. Both are kept
in bounded `deque`s (see the `history_size` setting). Windows are anchored to
the **newest sample timestamp**, not the wall clock, so stale histories don't
silently shrink to zero usable samples.

## Linear heating ETA

The default algorithm (`algorithm: "linear"`) assumes a constant heating rate.

### Theory

```text
rate = ΔT / Δt          (°C per second)
ETA  = (T_target - T_now) / rate
```

### How it works

`calculate_linear_eta(history, target, window_seconds=10.0)`:

1. Rejects non-finite targets and non-positive windows.
2. Filters the history to finite samples within the last `window_seconds`
   (relative to the newest sample) and needs at least 2 of them.
3. Takes the **first and last** sample of that window and computes the
   endpoint slope. It intentionally does not fit all points: printer heating
   is noisy at ~2 Hz sampling, and the endpoints over a short window average
   that noise well enough while staying O(n) with a tiny constant.
4. Requires the heater to actually be heating (`ΔT > 0`, `Δt > 0`) and below
   target (`target - T_now > 0`); otherwise returns `None`.

### Strengths and limits

- **Fast and robust** — works well during the initial heating ramp where the
  rate really is nearly constant.
- **Overestimates near the target** — real heaters slow down as they approach
  the setpoint (thermal losses grow with temperature), which the linear model
  can't see.

## Exponential heating ETA

Selectable via `algorithm: "exponential"`. Models the slowdown near the
target as a first-order exponential approach:

```text
T(t) = T_target - (T_target - T_0) * e^(-t/tau)
```

where `tau` is the thermal time constant.

### Fit and fallbacks

`calculate_exponential_eta(history, target, window_seconds=30.0)`:

1. Filters the window like the linear variant and drops duplicate
   timestamps. Fewer than 6 usable samples → **falls back to the linear
   estimate**.
2. Returns `None` when already at/above target or when the window shows no
   meaningful heating (rise ≤ 0.2 °C).
3. Returns `0.0` when the remaining delta is inside the convergence band
   `ε = 0.5 °C` (an exponential never mathematically *reaches* its asymptote,
   so "arrived" means "within ε").
4. Fits a line to `ln(target - T)` over time via least squares
   (`_linear_regression`). The slope `b` maps to the time constant
   `tau = -1/b`.
5. Sanity-checks the fit — all of these fall back to the linear estimate:
   - fewer than 6 log-transformed points, or a time span under 5 s
   - slope not meaningfully negative (`b >= -1e-4`, i.e. not converging)
   - implausible time constant (`tau > 2000 s`)
   - any `ValueError`/`ArithmeticError` from the math
6. Computes `ETA = tau * ln((target - T_now) / ε)`.
7. **Spike protection**: if the exponential ETA exceeds 5× the linear
   estimate, the linear value is returned instead. A noisy fit close to the
   asymptote can otherwise produce absurdly long countdowns.

### Accuracy trade-offs

- **More accurate near the target**, where the linear model overestimates.
- **Needs more data** (≥ 6 samples spanning ≥ 5 s) and degrades to linear
  when it can't get a trustworthy fit — the user always gets *some* estimate.

## Linear cooldown ETA

Used in `cooldown_mode: "threshold"` — countdown to a fixed per-heater
temperature (e.g. "bed safe to touch at 40 °C").

`calculate_cooldown_linear_eta(cooldown_history, goal_c, window_seconds=60.0)`
mirrors the linear heating estimator with inverted signs:

- The endpoint slope must be meaningfully negative (`< -1e-3 °C/s`); a heater
  that only drifts is treated as "not cooling" and gets no ETA.
- The current temperature must still be above the goal.
- The result is capped at 24 hours.

## Exponential cooldown ETA

Used in `cooldown_mode: "ambient"` — countdown until the heater is "near
ambient". Passive cooling follows Newton's law of cooling:

```text
T(t) = T_ambient + (T_0 - T_ambient) * e^(-t/tau)
```

`calculate_cooldown_exponential_eta(cooldown_history, ambient_c, goal_c, window_seconds=60.0)`:

1. Requires `goal_c > ambient_c` (the goal must be reachable by passive
   cooling) and at least 4 samples; fewer than 6 samples in the window →
   falls back to the linear cooldown estimate.
2. Fits `ln(T - T_ambient)` over time, requiring at least 4 usable points, a
   negative slope, and a plausible time constant (`0 < tau <= 20000 s`).
3. Computes `ETA = tau * ln((T_now - T_ambient) / (goal - T_ambient))`,
   capped at 24 hours.

The ambient temperature comes from the `cooldown_ambient_temp` setting when
set; otherwise the plugin learns a baseline from the lowest temperature
observed while the heater is off (see `_get_cooldown_ambient_c` in
`__init__.py`).

## How the plugin drives the estimators

The plugin (not the calculator) decides *when* an estimate is computed and
shown — see [Data flow](data-flow.md) for the full pipeline:

- Heating samples are recorded only while a heater has an active target and
  is more than `threshold_start` degrees below it; holding at temperature
  records nothing, so the fit window always reflects an actual ramp.
- Cooldown samples are kept in a **separate history** that is cleared on the
  heating → off transition, so old pre-heat data never pollutes the cooling
  fit.
- ETAs under 1 second are suppressed, and heaters not present in the active
  printer profile are skipped entirely.

### Edge cases

- **Target changes mid-heat**: history is *not* cleared; the window (10/30 s)
  ages the old ramp out quickly, and the persistence backoff schedule is
  reset (`target_change`) so fresh data is persisted soon.
- **Stalled heating**: no temperature rise in the window → `None` → the UI
  shows the idle state instead of a frozen countdown.
- **Overshoot / already there**: `remaining <= 0` → `None` (heating) or
  `T_now <= goal` → `None` (cooling).
- **Bad samples**: non-finite timestamps/temperatures are filtered out before
  fitting; math errors inside a fit degrade to the simpler estimator instead
  of raising into OctoPrint's callback thread.

## Configuration

Real settings that influence the algorithms (see
[Configuration](../reference/configuration.md) for the full list):

```yaml
plugins:
  temp_eta:
    algorithm: "linear" # or "exponential" (heating only)
    threshold_start: 5.0 # start showing ETA within this delta (°C)
    update_interval: 1.0 # seconds between frontend updates
    history_size: 60 # samples kept per heater
    enable_cooldown_eta: true
    cooldown_mode: "threshold" # or "ambient"
    cooldown_fit_window_seconds: 120 # cooldown fit window
    cooldown_ambient_temp: null # fixed ambient (ambient mode), else learned
```

## Performance

Both heating estimators run inside OctoPrint's temperature callback
(~2 Hz), so they are deliberately allocation-light and pure Python — no
numpy/scipy dependency:

- **Linear**: one filtered pass over ≤ `history_size` samples, then O(1)
  endpoint math.
- **Exponential**: one filtered pass plus a least-squares fit over the ≤ 60
  windowed samples; well under a millisecond on a Raspberry Pi class device.

## Testing

The estimators are pure functions, which keeps their tests trivial to write —
see [`tests/test_calculator.py`](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/tests/test_calculator.py):

```python
def test_heating_linear(self):
    """Constant 2 °C/s ramp, 30 °C remaining -> 15 s."""
    history = deque([(0.0, 20.0, 60.0), (5.0, 30.0, 60.0)])
    result = calculator.calculate_linear_eta(history, 60.0, window_seconds=10.0)
    self.assertAlmostEqual(result, 15.0, places=3)
```

See [Testing](../development/testing.md) for the full suite.

## References

- [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) - Original request
- Newton's Law of Cooling - [Wikipedia](https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling)
- Thermal Time Constant - [Engineering Toolbox](https://www.engineeringtoolbox.com/thermal-time-constant-d_1006.html)

## Next Steps

- [Python API](../api/python.md) - Implementation details
- [Settings](settings.md) - Configuration reference
- [Testing](../development/testing.md) - Algorithm tests
