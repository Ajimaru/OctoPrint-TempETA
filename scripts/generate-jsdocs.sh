#!/usr/bin/env bash
set -e

echo "Generating JavaScript API documentation..."

npx jsdoc2md \
  --configure jsdoc.json \
  "octoprint_temp_eta/static/js/**/*.js" \
  > docs/api/javascript.md

echo "Generated docs/api/javascript.md"
