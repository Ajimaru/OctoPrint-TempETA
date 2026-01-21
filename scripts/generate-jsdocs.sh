#!/usr/bin/env bash
set -e

echo "DEPRECATED: scripts/generate-jsdocs.sh is deprecated."
echo "Use the node-based generator: scripts/generate-jsdocs.js (run via pre-commit hook)."

# Try to delegate to the node generator if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"
NODE_SCRIPT="$PROJECT_ROOT/scripts/generate-jsdocs.js"

if command -v node >/dev/null 2>&1 && [ -f "$NODE_SCRIPT" ]; then
    echo "Delegating to node generator..."
    node "$NODE_SCRIPT"
    exit $?
else
    echo "Node generator not found; no action taken." >&2
    exit 0
fi
