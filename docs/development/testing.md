# Testing Guide

Comprehensive guide to testing OctoPrint-TempETA.

## Test Framework

The plugin uses **pytest** for testing with additional plugins:

- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `unittest.mock` - Mocking OctoPrint components

## Running Tests

### All Tests

```bash
pytest
```

### Specific Test File

```bash
pytest tests/test_calculator.py
```

### Specific Test

```bash
pytest tests/test_calculator.py::test_linear_heating
```

### With Coverage

```bash
pytest --cov=octoprint_temp_eta --cov-branch --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html
```

### Verbose Output

```bash
pytest -v
```

### Stop on First Failure

```bash
pytest -x
```

## Test Structure

```text
tests/
├── __init__.py
├── test_print_temp_eta.py    # Main plugin tests
├── test_calculator.py         # Calculator tests
└── test_mqtt_client.py        # MQTT client tests
```

## Writing Tests

### Calculator tests (pure functions)

The estimators in `octoprint_temp_eta/calculator.py` are stateless module
functions, so their tests need no plugin setup at all
(`tests/test_calculator.py` uses `unittest.TestCase` style):

```python
from collections import deque

from octoprint_temp_eta import calculator


class TestCalculateLinearETA(TestCase):
    def test_heating_linear(self):
        """Constant 2 °C/s ramp, 30 °C remaining -> 15 s."""
        history = deque([(0.0, 20.0, 60.0), (5.0, 30.0, 60.0)])
        result = calculator.calculate_linear_eta(history, 60.0)
        self.assertAlmostEqual(result, 15.0, places=3)

    def test_cooling_returns_none(self):
        """A falling temperature must not produce a heating ETA."""
        history = deque([(0.0, 60.0, 60.0), (5.0, 50.0, 60.0)])
        self.assertIsNone(calculator.calculate_linear_eta(history, 60.0))
```

### Plugin tests (stubbed OctoPrint)

`tests/test_print_temp_eta.py` instantiates the real `TempETAPlugin` and
injects small hand-written stubs (`DummyLogger`, `DummySettings`,
`DummyPluginManager`, `DummyPrinterProfileManager`) instead of OctoPrint's
components. A fixture wires them together:

```python
@pytest.fixture(name="temp_eta_plugin")
def fixture_temp_eta_plugin(...) -> TempETAPlugin:
    plugin = TempETAPlugin()
    plugin._logger = DummyLogger()
    plugin._settings = DummySettings(defaults=plugin.get_settings_defaults())
    plugin._plugin_manager = DummyPluginManager()  # records sent messages
    ...
    return plugin
```

Internal members are accessed via the `_get_attr`/`_set_attr`/`_call_attr`/
`_member` helpers so linters don't flag protected-member access in tests.

### Testing time-dependent code

Never `sleep()` in tests — monkeypatch `time.time` instead. The main test
file provides a `_set_time` helper for this:

```python
def test_callback_records_history(monkeypatch, temp_eta_plugin) -> None:
    _set_time(monkeypatch, 1000.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 25.0, "target": 200.0}}
    )
```

### Mocking paho-mqtt

`tests/test_mqtt_client.py` subclasses the wrapper with a test harness that
exposes internals, and patches the `mqtt` module where it is used:

```python
@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_configure_enabled_with_host(mock_mqtt, wrapper) -> None:
    mock_mqtt.Client.return_value = MagicMock()
    wrapper.configure({"mqtt_enabled": True, "mqtt_broker_host": "test-broker"})
    assert wrapper.get_internal_state("enabled")
```

### Testing "no estimate" paths

The estimators signal failure by returning `None` — assert on that rather
than expecting exceptions:

```python
def test_insufficient_data_empty_history(self):
    self.assertIsNone(calculator.calculate_linear_eta(deque(), 60.0))
```

## Test Data

### Creating Mock Data

Heating history samples are `(timestamp, actual_temp, target_temp)` tuples;
cooldown samples are `(timestamp, actual_temp)` tuples:

```python
import math
from collections import deque


def create_linear_heating(start=25.0, end=200.0, rate=2.0, samples=10):
    """Mock a constant-rate heating ramp."""
    history = deque(maxlen=60)
    for i in range(samples):
        t = float(i)
        history.append((t, start + rate * t, end))
    return history


def create_exponential_heating(start=25.0, end=200.0, tau=30.0, samples=20):
    """Mock a first-order exponential approach to the target."""
    history = deque(maxlen=60)
    for i in range(samples):
        t = float(i)
        temp = end - (end - start) * math.exp(-t / tau)
        history.append((t, temp, end))
    return history
```

## Coverage Requirements

Aim for:

- **Overall**: > 80%
- **Critical paths**: 100%
- **New code**: > 90%

Check coverage (per-module breakdown with missing line numbers):

```bash
pytest --cov=octoprint_temp_eta --cov-report=term-missing
```

## Continuous Integration

Tests run automatically on:

- Every push
- Every pull request
- Before merge

CI configuration: `.github/workflows/ci.yml`

## Testing with OctoPrint

### Virtual Printer

Test with OctoPrint's virtual printer:

```bash
# Install OctoPrint
pip install "OctoPrint>=1.11.0,<2"

# Install plugin
pip install -e .

# Run OctoPrint
octoprint serve --debug
```

In OctoPrint:

1. Enable the virtual printer (Settings → Serial Connection, or via the
   `devel.virtualPrinter` section in `config.yaml`)
2. Connect to the `VIRTUAL` port
3. Set temperatures (e.g. `M104 S200`) and observe the ETA

### Manual Testing Checklist

- [ ] Plugin loads without errors
- [ ] Settings page displays correctly
- [ ] ETA appears in temperature graph
- [ ] ETA appears in sidebar
- [ ] ETA updates in real-time
- [ ] Linear algorithm works
- [ ] Exponential algorithm works (if available)
- [ ] Heating ETA is accurate
- [ ] Cooling ETA is accurate
- [ ] MQTT publishing works (if enabled)
- [ ] Sounds play correctly (if enabled)
- [ ] Settings save and load correctly
- [ ] Translations work (if available)

## Performance Testing

The estimators run inside OctoPrint's ~2 Hz temperature callback, so keep an
eye on their cost when changing them:

```python
import cProfile
import pstats

def profile_linear_eta():
    """Profile the linear estimator over a full history."""
    history = create_linear_heating(samples=60)

    profiler = cProfile.Profile()
    profiler.enable()

    for _ in range(1000):
        calculator.calculate_linear_eta(history, 200.0)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)
```

For live monitoring against a real OctoPrint instance, see
`.development/monitor_octoprint_performance.sh`.

## Debugging Tests

### Run with Debugger

```bash
# Using pdb
pytest --pdb

# Break on first failure
pytest -x --pdb
```

### Print Debug Info

```python
def test_with_debug():
    """Test with debug output."""
    history = create_linear_heating()

    print(f"History length: {len(history)}")
    print(f"First sample: {history[0]}")
    print(f"Last sample: {history[-1]}")

    eta = calculator.calculate_linear_eta(history, 200.0)

    print(f"Calculated ETA: {eta}")

    assert eta is not None
```

Run with output:

```bash
pytest -s tests/test_calculator.py::test_with_debug
```

## Test Best Practices

1. **One assertion per test**: Keep tests focused
2. **Clear names**: Test name describes what it tests
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Independent tests**: Tests don't depend on each other
5. **Fast tests**: Keep test suite fast
6. **Mock external dependencies**: Don't rely on network, filesystem, etc.
7. **Test edge cases**: Empty lists, None values, negative numbers
8. **Document complex tests**: Add comments explaining logic

## Common Test Patterns

### Setup and Teardown

```python
def setup_module():
    """Run before all tests in module."""
    print("Setup module")

def teardown_module():
    """Run after all tests in module."""
    print("Teardown module")

def setup_function():
    """Run before each test function."""
    pass

def teardown_function():
    """Run after each test function."""
    pass
```

### Testing Time-Dependent Code

Patch `time.time` in the module under test (both the plugin module and the
calculator module read it):

```python
def _set_time(monkeypatch: pytest.MonkeyPatch, now: float) -> None:
    monkeypatch.setattr(octoprint_temp_eta.time, "time", lambda: now)
    monkeypatch.setattr(calc_module.time, "time", lambda: now)
```

## Test Documentation

Document tests with docstrings:

```python
def test_exponential_fitting():
    """
    Test exponential ETA with synthetic data.

    Creates temperature history following exponential heating model
    with tau=30s. Verifies that:
    1. Fitting succeeds with sufficient data
    2. ETA is within 10% of analytical solution
    3. Returns None with insufficient data
    """
    pass
```

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute tests
- [Algorithms](../architecture/algorithms.md) - What to test
- [Python API](../api/python.md) - API to test
