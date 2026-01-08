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
