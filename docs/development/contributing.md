# Contributing Guide

Thank you for your interest in contributing to OctoPrint-TempETA!

This guide expands on the [main CONTRIBUTING.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/CONTRIBUTING.md) with developer-specific details.

## Quick Links

- [GitHub Repository](https://github.com/Ajimaru/OctoPrint-TempETA)
- [Issue Tracker](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- [Pull Requests](https://github.com/Ajimaru/OctoPrint-TempETA/pulls)
- [Discussions](https://github.com/Ajimaru/OctoPrint-TempETA/discussions)

## Before You Start

- **One issue per PR**: Keep pull requests focused
- **Check existing issues**: Someone might be working on it
- **Discuss major changes**: Open an issue first for large features
- **Test your changes**: Include tests and verify manually
- **Follow conventions**: Match existing code style

## Development Setup

See [Getting Started](../getting-started.md) for detailed setup instructions.

Quick version:

```bash
# Clone
git clone https://github.com/Ajimaru/OctoPrint-TempETA.git
cd OctoPrint-TempETA

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e ".[develop]"
pre-commit install
```

## Workflow

### 1. Create a Branch

```bash
# Feature branch
git checkout -b feature/your-feature-name

# Bug fix branch
git checkout -b fix/issue-123-description
```

Branch naming:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/fixes

### 2. Make Changes

Follow coding standards:

- 4 spaces indentation (no tabs)
- English only
- Docstrings for public methods
- Type hints where applicable
- Comments explain WHY, not WHAT

Example:

```python
def calculate_eta(self, history: Deque, target: float) -> Optional[float]:
    """
    Calculate estimated time to target temperature.

    Uses linear extrapolation of recent temperature history.

    Args:
        history: Temperature history deque
        target: Target temperature in °C

    Returns:
        ETA in seconds, or None if insufficient data
    """
    if len(history) < 2:
        return None
    # ... implementation
```

### 3. Write Tests

Add tests for new functionality:

```python
# tests/test_calculator.py
def test_linear_heating():
    """Test linear algorithm with constant heating rate."""
    calculator = ETACalculator(algorithm="linear")
    history = deque()

    # Simulate heating at 2°C/s
    for i in range(10):
        history.append((i, 25 + i * 2, 200))

    eta = calculator.calculate_eta(history, 200)

    # Rate = 2°C/s, remaining = 175°C
    # Expected ETA = 87.5s
    assert abs(eta - 87.5) < 0.1
```

### 4. Run Tests

```bash
# All tests
pytest

# Specific test
pytest tests/test_calculator.py::test_linear_heating

# With coverage
pytest --cov=octoprint_temp_eta --cov-report=html

# View coverage
open htmlcov/index.html
```

### 5. Run Pre-commit Checks

```bash
# Run all checks
pre-commit run --all-files

# Format code
black octoprint_temp_eta tests
isort octoprint_temp_eta tests

# Lint
flake8 octoprint_temp_eta tests
```

### 6. Update Documentation

If your changes affect:

- **User behavior**: Update README.md
- **Settings**: Update settings documentation
- **API**: Update API docs
- **Architecture**: Update architecture docs

Generate updated docs:

```bash
./scripts/generate-jsdocs.sh
mkdocs build
```

### 7. Commit Changes

Write clear commit messages:

```bash
# Good commit message
git commit -m "Add exponential ETA algorithm

Implements exponential model for more accurate ETA near target.
Uses scipy for curve fitting. Falls back to linear if fitting fails.

Closes #123"

# Bad commit message
git commit -m "fix stuff"
```

Commit message format:

```
<type>: <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Add/fix tests
- `chore`: Maintenance

### 8. Push and Create PR

```bash
# Push branch
git push origin feature/your-feature-name

# Create PR on GitHub
# Fill in the PR template
```

## Pull Request Guidelines

### PR Title

Use the same format as commit messages:

```
feat: Add exponential ETA algorithm
fix: Correct ETA calculation for cooling
docs: Update installation instructions
```

### PR Description

Include:

1. **What**: What does this PR do?
2. **Why**: Why is this change needed?
3. **How**: How did you implement it?
4. **Testing**: How did you test it?
5. **Screenshots**: For UI changes
6. **Breaking changes**: List any breaking changes

Template:

```markdown
## Description

Adds exponential ETA algorithm for more accurate predictions near target temperature.

## Motivation

Linear algorithm is inaccurate in final approach to target due to thermal lag.

## Changes

- Added `exponential_eta()` method to calculator
- Added scipy dependency
- Updated settings to allow algorithm selection
- Added tests for exponential algorithm

## Testing

- [x] Unit tests pass
- [x] Manual testing with real printer
- [x] Tested with Python 3.11, 3.12, 3.13

## Screenshots

N/A - backend only change

## Breaking Changes

None
```

### Review Process

1. Automated checks must pass (CI, pre-commit)
2. Code review by maintainer
3. Address review comments
4. Squash commits if requested
5. Merge when approved

## Bug Reports

### Before Reporting

1. Check existing issues
2. Try latest version
3. Verify it's not a user error

### Report Template

```markdown
**OctoPrint Version**: 1.10.2
**Plugin Version**: 0.7.1
**Python Version**: 3.11.5
**OS**: Raspberry Pi OS (Debian 12)

**Description**

ETA shows incorrect value when heating bed.

**Steps to Reproduce**

1. Set bed target to 80°C
2. Observe ETA display
3. ETA shows "00:00" immediately

**Expected Behavior**

ETA should show realistic time estimate.

**Actual Behavior**

ETA shows zero immediately.

**Logs**
```

2024-01-15 10:30:00 - octoprint.plugins.temp_eta - DEBUG - ...

```

**Screenshots**

[Screenshot showing issue]
```

## Feature Requests

### Before Requesting

1. Check existing issues
2. Search discussions
3. Consider scope and feasibility

### Request Template

```markdown
**Problem**

Current ETA display is hard to read in bright light.

**Proposed Solution**

Add theme option for high-contrast display.

**Alternatives**

- Use user's system theme
- Add custom color picker

**Additional Context**

Common in outdoor 3D printing environments.
```

## Code Style

### Python

Follow PEP 8 and OctoPrint conventions:

```python
# Good
def calculate_eta(self, history, target):
    """Calculate ETA using linear extrapolation."""
    if len(history) < 2:
        return None

    rate = self._calculate_rate(history)
    remaining = target - history[-1][1]

    return remaining / rate if rate > 0 else None

# Bad
def calcETA(self,h,t):
    if len(h)<2:return None
    r=self._calcRate(h);rem=t-h[-1][1]
    return rem/r if r>0 else None
```

### JavaScript

Follow OctoPrint's JavaScript style:

```javascript
// Good
self.updateETA = function (heater, data) {
  var obs = self.heaters[heater];
  if (obs) {
    obs.eta(data.eta_seconds);
    obs.rate(data.rate);
  }
};

// Bad
self.updateETA = function (h, d) {
  var o = self.heaters[h];
  if (o) {
    o.eta(d.eta_seconds);
    o.rate(d.rate);
  }
};
```

### LESS/CSS

Use semantic naming:

```less
// Good
.temp-eta-sidebar {
  .heater-name {
    font-weight: bold;
  }

  .eta-value {
    color: @brand-primary;
  }
}

// Bad
.sidebar-1 {
  .text1 {
    font-weight: bold;
  }
  .text2 {
    color: blue;
  }
}
```

## Translation Contributions

See [Internationalization Guide](../frontend/i18n.md) for details.

To contribute translations:

```bash
# Initialize new language
pybabel init -i translations/messages.pot -d translations -l fr

# Edit translations/fr/LC_MESSAGES/messages.po

# Compile
pybabel compile -d translations

# Test in OctoPrint with French locale

# Submit PR with translation files
```

## Documentation Contributions

Documentation improvements are always welcome!

### Building Docs

```bash
# Install dependencies
pip install -r requirements-docs.txt
npm install

# Generate JS docs
./scripts/generate-jsdocs.sh

# Serve locally
mkdocs serve

# Build
mkdocs build
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Link to related pages
- Test all code examples

## Community

- Be respectful and constructive
- Help others in discussions
- Share your use cases
- Report issues promptly
- Celebrate successes

## Getting Help

- **Questions**: Use [GitHub Discussions](https://github.com/Ajimaru/OctoPrint-TempETA/discussions)
- **Bugs**: Open an [issue](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- **Security**: See [SECURITY.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the AGPLv3 license.

## Recognition

Contributors are listed in [AUTHORS.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/AUTHORS.md).

Thank you for contributing! 🎉

## Next Steps

- [Testing Guide](testing.md) - Writing and running tests
- [Release Process](release-process.md) - How releases are made
- [Architecture Overview](../architecture/overview.md) - Understanding the codebase
