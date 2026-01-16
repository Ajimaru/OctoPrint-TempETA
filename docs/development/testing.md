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

```
tests/
├── __init__.py
├── test_print_temp_eta.py    # Main plugin tests
├── test_calculator.py         # Calculator tests
└── test_mqtt_client.py        # MQTT client tests
```

## Writing Tests

### Basic Test

```python
def test_calculator_initialization():
    """Test calculator can be initialized."""
    calculator = ETACalculator(algorithm="linear")
    
    assert calculator.algorithm == "linear"
    assert calculator.min_rate == 0.1
    assert calculator.max_eta == 3600
```

### Test with Fixtures

```python
import pytest
from collections import deque

@pytest.fixture
def mock_history():
    """Create mock temperature history."""
    history = deque()
    for i in range(10):
        history.append((i, 25 + i * 2, 200))
    return history

def test_linear_eta(mock_history):
    """Test linear ETA calculation."""
    calculator = ETACalculator(algorithm="linear")
    eta = calculator.calculate_eta(mock_history, 200)
    
    assert eta is not None
    assert 80 < eta < 100  # ~87.5 seconds
```

### Parameterized Tests

```python
@pytest.mark.parametrize("algorithm,expected_range", [
    ("linear", (80, 100)),
    ("exponential", (70, 110)),
])
def test_algorithms(algorithm, expected_range):
    """Test different algorithms."""
    calculator = ETACalculator(algorithm=algorithm)
    history = create_heating_history()
    eta = calculator.calculate_eta(history, 200)
    
    assert expected_range[0] < eta < expected_range[1]
```

### Mocking OctoPrint

```python
from unittest.mock import MagicMock, patch

def test_plugin_initialization():
    """Test plugin initializes correctly."""
    # Mock OctoPrint components
    plugin = TempETAPlugin()
    plugin._logger = MagicMock()
    plugin._settings = MagicMock()
    plugin._plugin_manager = MagicMock()
    
    # Configure mocks
    plugin._settings.get.return_value = True
    
    # Test initialization
    plugin.on_after_startup()
    
    # Verify calls
    plugin._logger.info.assert_called()
```

### Testing Exceptions

```python
def test_invalid_algorithm():
    """Test calculator rejects invalid algorithm."""
    with pytest.raises(ValueError):
        ETACalculator(algorithm="invalid")
```

## Test Categories

### Unit Tests

Test individual components in isolation:

```python
def test_calculate_rate():
    """Test rate calculation."""
    calculator = ETACalculator()
    history = deque([
        (0, 25.0, 200),
        (5, 35.0, 200)
    ])
    
    rate = calculator._calculate_rate(history)
    
    assert abs(rate - 2.0) < 0.01  # 10°C / 5s = 2°C/s
```

### Integration Tests

Test component interactions:

```python
def test_plugin_eta_calculation():
    """Test plugin calculates and sends ETA."""
    plugin = setup_test_plugin()
    
    # Simulate temperature updates
    for i in range(10):
        plugin._on_temperature_update({
            "tool0": {"actual": 25 + i * 2, "target": 200}
        })
    
    # Verify ETA was calculated and sent
    assert plugin._last_eta["tool0"] is not None
```

### End-to-End Tests

Test complete workflows:

```python
def test_heating_workflow():
    """Test complete heating workflow."""
    plugin = setup_test_plugin()
    
    # Start heating
    plugin._on_event("PrintStarted", {})
    
    # Simulate heating
    for temp in range(25, 205, 5):
        plugin._on_temperature_update({
            "tool0": {"actual": temp, "target": 200}
        })
    
    # Verify completion
    assert plugin._heating_complete["tool0"]
    plugin._logger.info.assert_any_call("Heating complete")
```

## Test Data

### Creating Mock Data

```python
def create_linear_heating(start=25, end=200, rate=2.0, samples=10):
    """Create mock linear heating history."""
    history = deque()
    duration = (end - start) / rate
    
    for i in range(samples):
        t = (duration / samples) * i
        temp = start + rate * t
        history.append((t, temp, end))
    
    return history

def create_exponential_heating(start=25, end=200, tau=30, samples=20):
    """Create mock exponential heating history."""
    import math
    history = deque()
    
    for i in range(samples):
        t = i
        temp = end - (end - start) * math.exp(-t / tau)
        history.append((t, temp, end))
    
    return history
```

## Coverage Requirements

Aim for:

- **Overall**: > 80%
- **Critical paths**: 100%
- **New code**: > 90%

Check coverage:

```bash
pytest --cov=octoprint_temp_eta --cov-report=term-missing
```

Output:

```
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
octoprint_temp_eta/__init__.py       150      5    97%   234-238
octoprint_temp_eta/calculator.py      80      2    98%   56, 89
octoprint_temp_eta/mqtt_client.py     45      8    82%   67-74
----------------------------------------------------------------
TOTAL                                275     15    95%
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

1. Settings → Serial Connection → Additional serial ports: `/dev/ttyFAKE`
2. Connect to `/dev/ttyFAKE`
3. Set temperatures and observe ETA

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

### Profiling

```python
import cProfile
import pstats

def test_calculator_performance():
    """Profile calculator performance."""
    calculator = ETACalculator()
    history = create_large_history()
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(1000):
        calculator.calculate_eta(history, 200)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### Benchmarking

```python
import time

def test_calculation_speed():
    """Ensure calculation is fast enough."""
    calculator = ETACalculator()
    history = create_heating_history()
    
    start = time.time()
    
    for _ in range(100):
        calculator.calculate_eta(history, 200)
    
    elapsed = time.time() - start
    
    # Should complete 100 calculations in < 10ms
    assert elapsed < 0.01
```

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
    calculator = ETACalculator()
    history = create_heating_history()
    
    print(f"History length: {len(history)}")
    print(f"First sample: {history[0]}")
    print(f"Last sample: {history[-1]}")
    
    eta = calculator.calculate_eta(history, 200)
    
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

### Testing Async Code

```python
import asyncio

@pytest.mark.asyncio
async def test_async_operation():
    """Test async operation."""
    result = await async_function()
    assert result == expected
```

### Testing Time-Dependent Code

```python
from unittest.mock import patch
import time

def test_time_dependent():
    """Test time-dependent code."""
    with patch('time.time') as mock_time:
        mock_time.return_value = 1000
        
        # Test code that uses time.time()
        result = function_using_time()
        
        assert result == expected
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
