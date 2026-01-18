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
