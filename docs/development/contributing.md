# Contributing Guide

Developer-focused notes. For general info see the [main CONTRIBUTING.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/CONTRIBUTING.md).

## Links

- [Repository](https://github.com/Ajimaru/OctoPrint-TempETA) · [Issues](https://github.com/Ajimaru/OctoPrint-TempETA/issues) · [PRs](https://github.com/Ajimaru/OctoPrint-TempETA/pulls) · [Discussions](https://github.com/Ajimaru/OctoPrint-TempETA/discussions)

## Setup

```bash
git clone https://github.com/Ajimaru/OctoPrint-TempETA.git
cd OctoPrint-TempETA
python -m venv .venv && source .venv/bin/activate
pip install -e ".[develop]"
pre-commit install
```

See [Getting Started](../getting-started.md) for full instructions.

## Workflow

1. **Branch**: `feature/<name>`, `fix/<issue>-<desc>`, `docs/<name>`, `refactor/<name>`, `test/<name>`
2. **Code**: 4-space indent, English only, docstrings on public APIs, comments explain *why*
3. **Test**: `pytest` (add tests for new code, target ≥70% coverage)
4. **Lint**: `pre-commit run --all-files`
5. **Commit**: Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`)
6. **Push & PR**: one topic per PR, fill the PR template

### Common commands

```bash
pytest                                          # all tests
pytest tests/test_calculator.py::test_name      # single test
pytest --cov=octoprint_temp_eta --cov-report=html

black octoprint_temp_eta tests
isort octoprint_temp_eta tests
flake8 octoprint_temp_eta tests
```

## Code Style

### Python

PEP 8 + OctoPrint conventions. Type hints where useful.

```python
def calculate_eta(self, history: Deque, target: float) -> Optional[float]:
    """Calculate ETA via linear extrapolation. Returns seconds or None."""
    if len(history) < 2:
        return None
    rate = self._calculate_rate(history)
    remaining = target - history[-1][1]
    return remaining / rate if rate > 0 else None
```

### JavaScript

Match existing OctoPrint/Knockout style; use Knockout observables for reactive UI state.

### LESS/CSS

Use semantic, prefixed class names (`.temp-eta-*`). Edit LESS, never compiled CSS directly.

## Pull Requests

PR title uses commit-message format (`feat: …`, `fix: …`).

Include in the description:

- **What** & **why** the change is needed
- **How** it was implemented (key decisions)
- **Testing** done (unit / manual / Python versions)
- Screenshots for UI changes
- Any breaking changes

Checks before requesting review:

- [ ] Tests pass (`pytest`)
- [ ] Pre-commit clean (`pre-commit run --all-files`)
- [ ] Docs updated if behavior/API/settings changed

## Translations

```bash
pybabel init -i translations/messages.pot -d translations -l <lang>
# edit translations/<lang>/LC_MESSAGES/messages.po
pybabel compile -d translations
```

See [Internationalization Guide](../frontend/i18n.md).

## Documentation

```bash
pip install -r requirements-docs.txt
npm install
./scripts/generate-jsdocs.sh
mkdocs serve   # local preview
```

## License

Contributions are licensed under AGPLv3. Contributors are listed in [AUTHORS.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/AUTHORS.md).

## Next Steps

- [Testing Guide](testing.md)
- [Release Process](release-process.md)
- [Architecture Overview](../architecture/overview.md)
