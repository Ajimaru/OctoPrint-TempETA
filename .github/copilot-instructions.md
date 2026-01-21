# GitHub Copilot Instructions - OctoPrint Temperature ETA Plugin

**Issue**: [#469](https://github.com/OctoPrint/OctoPrint/issues/469) - Show ETA for bed/hotend heating
**Target**: OctoPrint 1.10.2+, Python 3.7+ | Implements 2014 feature request

## Code Standards (CRITICAL)

**Docs**: https://docs.octoprint.org/en/main/plugins/index.html | Contributing: https://github.com/OctoPrint/OctoPrint/blob/main/CONTRIBUTING.md

**Template Autoescape**: [How do I improve my plugin's security by enabling autoescape?](https://faq.octoprint.org/plugin-autoescape)

### Code Style (OctoPrint Standard)

- **Indentation**: 4 spaces (NO TABS)
- **Language**: English only (code, comments, docs)
- **Docstrings**: All public methods/classes
- **Comments**: Explain WHY, not WHAT
- **Line length**: 120 chars max (black)
- **No dead code**: Remove all commented-out experiments
- **Import order**: stdlib → third-party → octoprint → local

### Repository communication (English only)

### change /print_temp_eta/CHANGELOG.md only on order

- **All public-facing repository communication must be in English only**: GitHub Issues, Pull Requests, Discussions, Wiki pages, and Security advisories.
- If a user writes in another language, respond in English and keep technical terms consistent.

**When generating code**: Follow OctoPrint standards, use English, include docstrings, test edge cases, ensure thread safety, keep performance in mind.

### Testing: pytest, min 70% coverage, test edge cases, mock OctoPrint internals

### Temperature Callback (Called ~2Hz)

### Thread Safety (CRITICAL)

### Logging (use self.\_logger)

```python
self._logger.info("ETA started")
self._logger.debug("Rate: %.2f °C/s", rate)
self._logger.error("Failed: %s", str(e))
```

## Algorithm Implementation

### Linear ETA (Default)

```python
def calculate_linear_eta(history, target):
    """Returns seconds to target, None if insufficient data."""
    if len(history) < 2:
        return None

    # Use last 10 seconds of data
    recent = [h for h in history if h[0] > time.time() - 10]
    if len(recent) < 2:
        return None

    # rate = ΔT / Δt (°C per second)
    rate = (recent[-1][1] - recent[0][1]) / (recent[-1][0] - recent[0][0])

    if rate <= 0:
        return None

    remaining = target - recent[-1][1]
    return remaining / rate
```

### Exponential ETA (Advanced)

```python
def calculate_exponential_eta(history, target):
    # Model: T(t) = T_final - (T_final - T_0) * e^(-t/tau)
    # Implementation in calculator.py
    pass
```

## Internationalization

**Babel Translation**:

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations -l de
pybabel compile -d translations
```

**In Code**:

```python
from flask_babel import gettext
message = gettext("Heating to {target}°C, ETA: {eta}").format(target=X, eta=Y)
```

**Languages**: English (en) + German (de)

## Critical Rules

1. **DO NOT** use `print()` → use `self._logger`
2. **DO NOT** edit CSS directly → Edit LESS and compile
3. **DO NOT** block callback → Keep it fast (<10ms)
4. **DO NOT** assume temp increases → Handle cooling, target changes
5. **DO NOT** forget thread safety → Use locks for shared data
6. **DO NOT** use globals → Use instance variables only
7. **DO NOT** hardcode strings → Use i18n for user-facing text
8. **DO NOT** forget disabled heaters → Check if target > 0

## Performance

- Callback processing: < 10ms (2Hz)
- Frontend updates: 1Hz default
- Memory: < 5MB for history
- Cleanup: Remove data older than 60 seconds

## Development Workflow

```bash
# Branch: wip/feature-name or fix/issue-description
# Commit: "Add ETA calculation" (imperative mood)
# Before commit: pytest && pre-commit run --all-files
```

## Files to Ignore (Don't Commit)

`.development/`, `venv/`, `__pycache__/`, `.pytest_cache/`, `.coverage/`, `.idea/`, `.vscode/`

## Key References

- Issue #469: https://github.com/OctoPrint/OctoPrint/issues/469
- Plugin Docs: https://docs.octoprint.org/en/main/plugins/
- Mixins: https://docs.octoprint.org/en/main/plugins/mixins.html
- Contributing: https://github.com/OctoPrint/OctoPrint/blob/main/CONTRIBUTING.md
- Knockout.js: https://knockoutjs.com/documentation/introduction.html
