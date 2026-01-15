#!/usr/bin/env bash
set -e

echo "Generating JavaScript API documentation..."

# Check if JS files exist
if ! ls octoprint_temp_eta/static/js/*.js 1> /dev/null 2>&1; then
    echo "Warning: No JavaScript files found"
    echo "# JavaScript API" > docs/api/javascript.md
    echo "" >> docs/api/javascript.md
    echo "No JavaScript files found for documentation generation." >> docs/api/javascript.md
    exit 0
fi

# Generate documentation
npx jsdoc2md \
  --configure jsdoc.json \
  "octoprint_temp_eta/static/js/**/*.js" \
  > docs/api/javascript.md

# Check if output is empty (no JSDoc comments)
if [ ! -s docs/api/javascript.md ]; then
    echo "Warning: No JSDoc comments found in JavaScript files"
    cat > docs/api/javascript.md << 'EOF'
# JavaScript API

This page will contain auto-generated JavaScript API documentation.

## Current Status

The JavaScript source files exist but don't yet have JSDoc comments. To generate documentation:

1. Add JSDoc comments to JavaScript files
2. Run `./scripts/generate-jsdocs.sh`

## Example JSDoc Comment

```javascript
/**
 * Calculate ETA for a heater.
 * @param {string} heater - Heater name (e.g., "tool0", "bed")
 * @param {Object} data - Temperature data
 * @param {number} data.current - Current temperature
 * @param {number} data.target - Target temperature
 * @returns {number} ETA in seconds, or null if unavailable
 */
function calculateETA(heater, data) {
    // Implementation
}
```

## Source Files

- `octoprint_temp_eta/static/js/temp_eta.js`

## Manual Overview

For now, see the [manual overview](javascript.md) in this directory.
EOF
fi

echo "Generated docs/api/javascript.md"
