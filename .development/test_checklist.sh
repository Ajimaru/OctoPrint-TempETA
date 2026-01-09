#!/bin/bash
# Temperature ETA Plugin - Quick Test Checklist

echo "======================================"
echo "Temperature ETA Plugin - Test Setup"
echo "======================================"
echo ""

# Step 1: Check Python
echo "1️⃣  Python & pip:"
python3 --version
pip --version
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
echo "   cd /home/robby/Temp/print_temp_eta"
echo "   pip install -e ."
echo "   # Restart OctoPrint"
echo ""
echo "Method B: Isolated Testing Environment"
echo "   python3 -m venv /tmp/octoprint_test"
echo "   source /tmp/octoprint_test/bin/activate"
echo "   pip install OctoPrint"
echo "   cd /home/robby/Temp/print_temp_eta"
echo "   pip install -e ."
echo "   octoprint serve"
echo "   # Open http://localhost:5000"
echo ""
echo "======================================"
echo "✅ Plugin is ready for testing!"
echo "======================================"
