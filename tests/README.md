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

The main unit test suite lives in `tests/test_print_temp_eta.py`.

MQTT integration logic is covered in `tests/test_mqtt_client.py`.

Notes:

- Tests are pure unit tests and do **not** require a running OctoPrint instance.
- Time is controlled via `monkeypatch` (no `sleep()` calls) to keep the suite fast and deterministic.

### Integration Tests

- **Virtual Printer:** Manual testing with OctoPrint's Virtual Printer plugin
- **Real Printer:** Beta testing with a real printer
- **Browser Testing:** Chrome, Firefox, Safari

### Performance Tests

- Temperature callback should take < 1 ms
- Frontend updates should not block
- Monitor memory usage during 24-hour operation

Refer to OctoPrint's [plugin development documentation](https://docs.octoprint.org/en/latest/plugins/development.html#testing) for more details.
