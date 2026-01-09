# Test Suite

This directory contains the test suite for the Temperature ETA plugin.

## Running Tests

Install test dependencies:

```bash
pip install -e ".[develop]"
```

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=octoprint_temp_eta --cov-report=html
```

## Writing Tests

Follow OctoPrint's testing guidelines:

- Use pytest for new tests
- Ensure good code coverage
- Test edge cases
- Mock external dependencies
- Run unit tests
- Check code coverage (aim for >70%)
- Performance profiling

### Unit Tests

```python
# tests/test_temp_eta.py
import pytest
import time
from octoprint_temp_eta import TempETAPlugin

class MockPrinter:
    def register_callback(self, callback):
        pass

class TestTempETAPlugin:

    @pytest.fixture
    def plugin(self):
        p = TempETAPlugin()
        p._printer = MockPrinter()
        p._settings = MockSettings()
        p._logger = MockLogger()
        return p

    def test_eta_calculation_heating(self, plugin):
        """Test ETA during heating"""
        # Simulate heating from 20°C to 220°C
        plugin.on_printer_add_temperature({
            "tool0": {"actual": 20.0, "target": 220.0}
        })
        time.sleep(0.1)

        for temp in range(30, 220, 10):
            time.sleep(0.5)
            plugin.on_printer_add_temperature({
                "tool0": {"actual": float(temp), "target": 220.0}
            })

        eta_data = plugin.get_eta_data()
        assert "tool0" in eta_data
        assert eta_data["tool0"]["eta_seconds"] > 0
        assert eta_data["tool0"]["eta_seconds"] < 100  # Reasonable range

    def test_no_eta_when_at_target(self, plugin):
        """Test no ETA when at target temperature"""
        plugin.on_printer_add_temperature({
            "tool0": {"actual": 220.0, "target": 220.0}
        })

        eta_data = plugin.get_eta_data()
        assert "tool0" not in eta_data

    def test_multiple_heaters(self, plugin):
        """Test tracking multiple heaters"""
        plugin.on_printer_add_temperature({
            "tool0": {"actual": 100.0, "target": 220.0},
            "bed": {"actual": 30.0, "target": 60.0}
        })

        time.sleep(1)

        plugin.on_printer_add_temperature({
            "tool0": {"actual": 110.0, "target": 220.0},
            "bed": {"actual": 35.0, "target": 60.0}
        })

        eta_data = plugin.get_eta_data()
        assert "tool0" in eta_data
        assert "bed" in eta_data
```

### Integration Tests

- **Virtual Printer:** Manual testing with OctoPrint's Virtual Printer plugin
- **Real Printer:** Beta testing with a real printer
- **Browser Testing:** Chrome, Firefox, Safari

### Performance Tests

- Temperature callback should take < 1 ms
- Frontend updates should not block
- Monitor memory usage during 24-hour operation

Refer to OctoPrint's [plugin development documentation](https://docs.octoprint.org/en/master/plugins/development.html#testing) for more details.
