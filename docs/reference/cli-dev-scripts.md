# Development Scripts Reference

Reference for all development and maintenance scripts in the OctoPrint-TempETA project.

## Scripts Directory

All scripts are located in the `scripts/` directory:

```
scripts/
├── generate-jsdocs.sh    # Generate JavaScript API docs
└── (future scripts)
```

## generate-jsdocs.sh

Generate JavaScript API documentation from JSDoc comments.

### Usage

```bash
./scripts/generate-jsdocs.sh
```

Or via npm:

```bash
npm run docs:js
```

### What It Does

1. Reads JavaScript files from `octoprint_temp_eta/static/js/`
2. Extracts JSDoc comments
3. Generates Markdown documentation
4. Saves to `docs/api/javascript.md`

### Requirements

- Node.js 20+
- jsdoc package
- jsdoc-to-markdown package

Install:

```bash
npm install
```

### Output

Creates `docs/api/javascript.md` with:

- Function signatures
- Parameter descriptions
- Return values
- Usage examples

### Troubleshooting

**Error: "npx: command not found"**

Install Node.js:

```bash
# Ubuntu/Debian
sudo apt install nodejs npm

# macOS
brew install node

# Or download from nodejs.org
```

**Error: "jsdoc2md: not found"**

Install dependencies:

```bash
npm install
```

**No output generated**

Check JavaScript files have JSDoc comments:

```javascript
/**
 * Calculate ETA for heater.
 * @param {string} heater - Heater name
 * @param {Object} data - Temperature data
 * @returns {number} ETA in seconds
 */
function calculateETA(heater, data) {
  // ...
}
```

## Python Scripts

### Babel Commands

Extract translatable strings:

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
```

Initialize new language:

```bash
pybabel init -i translations/messages.pot -d translations -l fr
```

Update existing translations:

```bash
pybabel update -i translations/messages.pot -d translations
```

Compile translations:

```bash
pybabel compile -d translations
```

### pytest Commands

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=octoprint_temp_eta --cov-branch --cov-report=html
```

Run specific test:

```bash
pytest tests/test_calculator.py::test_linear_heating
```

### Pre-commit Commands

Run all hooks:

```bash
pre-commit run --all-files
```

Install hooks:

```bash
pre-commit install
```

Update hooks:

```bash
pre-commit autoupdate
```

### Code Formatting

Format with black:

```bash
black octoprint_temp_eta tests
```

Sort imports:

```bash
isort octoprint_temp_eta tests
```

Lint with flake8:

```bash
flake8 octoprint_temp_eta tests
```

### Build Commands

Build package:

```bash
python -m build
```

Install in editable mode:

```bash
pip install -e ".[develop]"
```

Clean build artifacts:

```bash
rm -rf build/ dist/ *.egg-info
```

## Documentation Commands

### MkDocs

Serve documentation locally:

```bash
mkdocs serve
```

Access at: http://localhost:8000

Build documentation:

```bash
mkdocs build
```

Output in: `site/`

Deploy to GitHub Pages:

```bash
mkdocs gh-deploy
```

### Generate All Docs

Complete documentation generation:

```bash
# Generate JavaScript docs
./scripts/generate-jsdocs.sh

# Build MkDocs site
mkdocs build
```

## Git Commands

### Common Workflows

Create feature branch:

```bash
git checkout -b feature/your-feature
```

Commit changes:

```bash
git add .
git commit -m "feat: Add new feature"
```

Push branch:

```bash
git push origin feature/your-feature
```

Update from main:

```bash
git checkout main
git pull
git checkout feature/your-feature
git rebase main
```

### Release Workflow

Create release branch:

```bash
git checkout -b release/v0.8.0
```

Tag release:

```bash
git tag -a v0.8.0 -m "Release v0.8.0"
git push origin v0.8.0
```

## CI/CD Commands

### Local CI Simulation

Run tests like CI:

```bash
# Install dependencies
pip install -e ".[develop]"

# Run tests
pytest

# Run pre-commit
pre-commit run --all-files

# Build package
python -m build
```

### GitHub Actions

Trigger workflow manually:

```bash
# Using GitHub CLI
gh workflow run ci.yml

# Or via web interface
# Actions → Select workflow → Run workflow
```

## Maintenance Scripts

### Clean Development Environment

Remove all generated files:

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove test cache
rm -rf .pytest_cache
rm -rf .coverage htmlcov

# Remove build artifacts
rm -rf build dist *.egg-info

# Remove docs build
rm -rf site

# Remove node_modules
rm -rf node_modules
```

### Reset Virtual Environment

```bash
# Deactivate
deactivate

# Remove
rm -rf venv

# Recreate
python -m venv venv
source venv/bin/activate
pip install -e ".[develop]"
```

## Development Helpers

### Quick Test

Test changes quickly:

```bash
# Format, lint, test
black octoprint_temp_eta tests && \
isort octoprint_temp_eta tests && \
pytest -q
```

### Watch Tests

Auto-run tests on file change:

```bash
pip install pytest-watch
ptw -- -q
```

### Coverage Report

Generate and view coverage:

```bash
pytest --cov=octoprint_temp_eta --cov-report=html
open htmlcov/index.html
```

## OctoPrint Development

### Install in OctoPrint

```bash
# In OctoPrint venv
source ~/oprint/bin/activate

# Install plugin
pip install -e .

# Run OctoPrint
octoprint serve --debug
```

### Plugin Logs

View plugin logs:

```bash
tail -f ~/.octoprint/logs/octoprint.log | grep temp_eta
```

### Restart OctoPrint

```bash
# If running as service
sudo systemctl restart octoprint

# If running manually
# Press Ctrl+C, then run again
octoprint serve --debug
```

## Utility Scripts

### Check Version

```bash
python -c "import octoprint_temp_eta; print(octoprint_temp_eta.__version__)"
```

### Validate Config

```bash
python -c "
import yaml
with open('mkdocs.yml') as f:
    config = yaml.safe_load(f)
    print('Valid configuration')
"
```

### Count Lines of Code

```bash
# Python
find octoprint_temp_eta -name "*.py" -exec wc -l {} + | tail -1

# JavaScript
find octoprint_temp_eta/static/js -name "*.js" -exec wc -l {} + | tail -1

# Tests
find tests -name "*.py" -exec wc -l {} + | tail -1
```

## Environment Setup

### Python Environment

```bash
# Check Python version
python --version

# Create venv
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install
pip install -e ".[develop]"
```

### Node Environment

```bash
# Check Node version
node --version
npm --version

# Install dependencies
npm install

# Run script
npm run docs:js
```

## Troubleshooting Scripts

### Permission Issues

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Fix git hooks
chmod +x .githooks/*
```

### Dependency Issues

```bash
# Update pip
pip install --upgrade pip

# Reinstall dependencies
pip install --force-reinstall -e ".[develop]"

# Clear pip cache
pip cache purge
```

### Import Issues

```bash
# Verify installation
pip list | grep OctoPrint-TempETA

# Check import
python -c "import octoprint_temp_eta"

# Reinstall
pip uninstall OctoPrint-TempETA
pip install -e ".[develop]"
```

## Custom Scripts

You can add custom scripts to the `scripts/` directory:

```bash
#!/usr/bin/env bash
# scripts/my-script.sh

set -e

echo "Running custom script..."
# Your commands here
```

Make executable:

```bash
chmod +x scripts/my-script.sh
```

## Next Steps

- [Contributing Guide](../development/contributing.md) - Development workflow
- [Testing Guide](../development/testing.md) - Testing commands
- [Release Process](../development/release-process.md) - Release commands
- [Getting Started](../getting-started.md) - Setup instructions
