#!/usr/bin/env bash
set -euo pipefail

# Helper to run pre-commit checks and only commit if they all pass.
# Usage: .development/commit-if-clean.sh -m "Commit message"

MSG=""
while getopts ":m:" opt; do
  case ${opt} in
    m ) MSG=$OPTARG ;;
    \? ) echo "Usage: $0 -m \"commit message\"" ; exit 2 ;;
  esac
done

if [ -z "${MSG}" ]; then
  echo "Commit message is required. Usage: $0 -m \"commit message\"" >&2
  exit 2
fi

echo "Running pre-commit hooks..."
if ! pre-commit run --all-files; then
  echo "Pre-commit checks failed — aborting commit." >&2
  exit 1
fi

# If pre-commit fixed files (e.g. Prettier), refuse to auto-commit.
# This ensures we don't silently commit auto-fixes when hooks modify files.
if [ -n "$(git status --porcelain)" ]; then
  echo "pre-commit made changes to the working tree. Please review and commit them manually:" >&2
  git --no-pager status --porcelain
  echo "Run 'git add -A && git commit -m \"<msg>\"' after reviewing, or re-run this helper." >&2
  exit 2
fi

echo "Staging all changes and committing..."
git add -A
git commit -m "${MSG}"
echo "Committed."
