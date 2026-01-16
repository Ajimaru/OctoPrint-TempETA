# Getting Started

This guide will help you set up a development environment for OctoPrint-TempETA.

## Prerequisites

- Python 3.11 or higher
- Node.js 20 or higher (for documentation generation)
- Git
- A code editor (VS Code recommended)

## Clone the Repository

```bash
git clone https://github.com/Ajimaru/OctoPrint-TempETA.git
cd OctoPrint-TempETA
```

## Set Up Python Environment

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install plugin with development dependencies
pip install -e ".[develop]"

# Install documentation dependencies
pip install -r requirements-docs.txt
```

## Install Node.js Dependencies

For JavaScript API documentation generation:

```bash
npm install
```

## Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=octoprint_temp_eta --cov-branch --cov-report=html

# Run specific test
pytest tests/test_calculator.py
```

## Code Quality

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```

### Code Style

This project follows:

- **Black** for code formatting (120 char line length)
- **isort** for import sorting
- **flake8** for linting
- **4 spaces** for indentation (no tabs)

Format code:

```bash
black octoprint_temp_eta tests
isort octoprint_temp_eta tests
```

## Build Documentation

### Generate JavaScript API Docs

```bash
./scripts/generate-jsdocs.sh
```

### Serve Documentation Locally

```bash
mkdocs serve
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

### Build Documentation

```bash
mkdocs build
```

Output will be in the `site/` directory.

## Project Structure

```
OctoPrint-TempETA/
├── octoprint_temp_eta/          # Main plugin code
│   ├── __init__.py              # Plugin entry point
│   ├── calculator.py            # ETA calculation algorithms
│   ├── mqtt_client.py           # MQTT integration
│   ├── static/                  # Frontend assets
│   │   └── js/
│   │       └── temp_eta.js      # Frontend JavaScript
│   └── templates/               # HTML templates
├── tests/                       # Test suite
├── docs/                        # Documentation source
├── scripts/                     # Utility scripts
├── translations/                # i18n files
├── requirements.txt             # Runtime dependencies
├── requirements-docs.txt        # Documentation dependencies
├── pyproject.toml              # Project configuration
├── mkdocs.yml                  # Documentation config
└── package.json                # Node.js dependencies
```

## Next Steps

- Read the [Architecture Overview](architecture/overview.md) to understand the system design
- Check out the [Contributing Guide](development/contributing.md) for contribution guidelines
- Explore the [Python API](api/python.md) and [JavaScript API](api/javascript.md) references
- Run the [test suite](development/testing.md) to ensure everything works

## Common Tasks

### Adding a New Feature

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD approach)
3. Implement the feature
4. Run tests and pre-commit checks
5. Update documentation
6. Submit a pull request

### Debugging

The plugin uses OctoPrint's logging system. Enable debug logging in OctoPrint settings:

```
Settings → Logging → Set octoprint.plugins.temp_eta to DEBUG
```

### Testing with OctoPrint

To test the plugin with a real OctoPrint instance:

```bash
# Install OctoPrint in your venv
pip install "OctoPrint>=1.11.0,<2"

# Install the plugin in development mode
pip install -e .

# Run OctoPrint
octoprint serve
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you've installed the plugin in editable mode:

```bash
pip install -e ".[develop]"
```

### Test Failures

Check that all dependencies are installed:

```bash
pip list
```

### Documentation Build Fails

Ensure all documentation dependencies are installed:

```bash
pip install -r requirements-docs.txt
npm install
```

## Getting Help

- Check the [Contributing Guide](development/contributing.md)
- Search existing [GitHub Issues](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- Open a new issue if you can't find a solution
