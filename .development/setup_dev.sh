#!/usr/bin/env bash
# Setup script for OctoPrint Temperature ETA plugin development.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Setting up development environment..."

# Check if Python 3.7+ is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is not installed" >&2
    exit 1
fi

python3 - <<'PY'
import sys

major, minor = sys.version_info[:2]
if (major, minor) < (3, 7):
    raise SystemExit(f"ERROR: Python {major}.{minor} found, but 3.7+ is required")

print(f"Found Python {major}.{minor}")
PY

VENV_DIR="$REPO_ROOT/venv"

# Create virtual environment
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment at: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists: $VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install plugin with development dependencies
echo "Installing plugin (editable) with development dependencies..."
python -m pip install -e ".[develop]"

# Enable repo-local git hooks (post-commit build on version bump)
echo "Enabling repository git hooks (.githooks)..."
if command -v git >/dev/null 2>&1; then
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        chmod +x .githooks/post-commit 2>/dev/null || true
        git config core.hooksPath .githooks
        echo "Git hooks enabled (core.hooksPath=.githooks)"
    else
        echo "WARNING: Not a git repository, skipping git hooks setup"
    fi
else
    echo "WARNING: git not found, skipping git hooks setup"
fi

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit install
else
    echo "WARNING: pre-commit not found, skipping hook installation"
    echo "         Install via: python -m pip install pre-commit (recommended)"
    echo "         or system-wide: sudo apt install pre-commit"
fi

# Run pre-commit on all files (optional, can take time)
echo "Running initial pre-commit checks..."
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --all-files || echo "WARNING: Some pre-commit checks failed (common on first run)."
else
    echo "WARNING: pre-commit not found, skipping initial checks"
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run tests: pytest"
echo "  3. Run checks (if installed): pre-commit run --all-files"
echo ""
echo "See CONTRIBUTING.md for more information."
