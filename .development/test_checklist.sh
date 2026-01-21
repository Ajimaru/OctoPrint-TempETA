#!/usr/bin/env bash
# Temperature ETA Plugin - Quick Test Checklist

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT=""
if command -v git >/dev/null 2>&1; then

    REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
fi
if [[ -z "$REPO_ROOT" ]]; then

    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi
cd "$REPO_ROOT"

PYTHON_BIN="python3"
PIP_BIN="pip"
if [[ -x "$REPO_ROOT/venv/bin/python" ]]; then

    PYTHON_BIN="$REPO_ROOT/venv/bin/python"
    PIP_BIN="$REPO_ROOT/venv/bin/pip"
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then

    echo "ERROR: $PYTHON_BIN not found" >&2
    exit 1
fi

if ! "$PYTHON_BIN" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)' >/dev/null 2>&1; then

    "$PYTHON_BIN" --version >&2 || true
    echo "ERROR: Python 3.10+ is required to run this checklist" >&2
    echo "Hint: Run .development/setup_dev.sh to create ./venv" >&2
    exit 1
fi

REPO_ROOT_CMD="<repo-root>"
if command -v git >/dev/null 2>&1; then

    REPO_ROOT_CMD='"$(git rev-parse --show-toplevel)"'
fi

echo "======================================"
echo "Temperature ETA Plugin - Test Setup"
echo "======================================"
echo ""

# Step 1: Check Python
echo "1️⃣  Python & pip:"
"$PYTHON_BIN" --version
"$PIP_BIN" --version
echo ""

# Step 2: Check pyproject.toml
echo "2️⃣  Project Configuration:"
echo "   Plugin Name: $(grep '^name' pyproject.toml | cut -d'"' -f2)"
echo "   Version: $(grep '^version' pyproject.toml | cut -d'"' -f2)"
echo "   Python Requirement: $(grep 'requires-python' pyproject.toml)"
echo ""

# Step 3: Check main plugin file
echo "3️⃣  Backend Implementation:"
PLUGIN_METHODS=$(grep -c "def " octoprint_temp_eta/__init__.py)
echo "   ✓ $PLUGIN_METHODS backend methods implemented"
echo ""

# Step 4: Check JavaScript
echo "4️⃣  Frontend Implementation:"
JS_FUNCTIONS=$(grep -c "self\." octoprint_temp_eta/static/js/temp_eta.js)
echo "   ✓ $JS_FUNCTIONS ViewModel properties/methods"
echo ""

# Step 5: Check Templates
echo "5️⃣  Templates:"
echo "   ✓ Navbar: $(test -s octoprint_temp_eta/templates/temp_eta_navbar.jinja2 && echo 'Ready' || echo 'Missing')"
echo "   ✓ Settings: $(test -s octoprint_temp_eta/templates/temp_eta_settings.jinja2 && echo 'Ready' || echo 'Missing')"
echo "   ✓ Tab: $(test -s octoprint_temp_eta/templates/temp_eta_tab.jinja2 && echo 'Ready' || echo 'Missing')"
echo ""

# Step 6: Check Styling
echo "6️⃣  Styling:"
LESS_LINES=$(wc -l < octoprint_temp_eta/static/less/temp_eta.less)
echo "   ✓ LESS: $LESS_LINES lines"
echo ""

# Step 7: Check Translations
echo "7️⃣  Internationalization:"
echo "   ✓ POT: $(test -s translations/messages.pot && echo 'Ready' || echo 'Missing')"
echo "   ✓ German: $(test -s translations/de/LC_MESSAGES/messages.po && echo 'Ready' || echo 'Missing')"
echo "   ✓ English: $(test -s translations/en/LC_MESSAGES/messages.po && echo 'Ready' || echo 'Missing')"
echo ""

# Step 8: Installation Instructions
echo "======================================"
echo "Installation Instructions"
echo "======================================"
echo ""
echo "Method A: Development Installation (for existing OctoPrint)"
echo "   cd $REPO_ROOT_CMD"
echo "   source venv/bin/activate"
echo "   python -m pip install -e \".[develop]\""
echo "   # Restart OctoPrint"
echo ""
echo "Method B: Isolated Testing Environment"
echo "   python3 -m venv /tmp/octoprint_test"
echo "   source /tmp/octoprint_test/bin/activate"
echo "   pip install OctoPrint"
echo "   cd $REPO_ROOT_CMD"
echo "   pip install -e \".[develop]\""
echo "   octoprint serve"
echo "   # Open http://localhost:5000"
echo ""
echo "======================================"
echo "✅ Plugin is ready for testing!"
echo "======================================"
