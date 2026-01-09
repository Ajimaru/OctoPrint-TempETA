#!/usr/bin/env bash
set -euo pipefail

# Post-commit hook: if the project version changed in this commit, build fresh
# artifacts into dist/ (wheel + sdist via build, plus a zip derived from sdist).

log() {
  printf '[temp-eta post-commit] %s\n' "$*"
}

get_version_from_pyproject() {
  local file_path="$1"

  python3 - "$file_path" <<'PY'
import sys

path = sys.argv[1]
raw = open(path, 'rb').read()

try:
    import tomllib  # py3.11+
    data = tomllib.loads(raw.decode('utf-8'))
except ModuleNotFoundError:
    import tomli  # type: ignore
    data = tomli.loads(raw.decode('utf-8'))

version = data.get('project', {}).get('version')
if not version:
    raise SystemExit('Unable to determine version from pyproject.toml')

print(version)
PY
}

get_version_from_pyproject_content() {
  python3 - <<'PY'
import sys

raw = sys.stdin.buffer.read()

try:
    import tomllib
    data = tomllib.loads(raw.decode('utf-8'))
except ModuleNotFoundError:
    import tomli  # type: ignore
    data = tomli.loads(raw.decode('utf-8'))

version = data.get('project', {}).get('version')
if not version:
    raise SystemExit(1)
print(version)
PY
}

create_zip_from_sdist() {
  local tar_path="$1"
  local zip_path="$2"

  python3 - "$tar_path" "$zip_path" <<'PY'
import sys
import tarfile
import zipfile

from pathlib import Path

tar_path = Path(sys.argv[1])
zip_path = Path(sys.argv[2])

zip_path.parent.mkdir(parents=True, exist_ok=True)

with tarfile.open(tar_path, 'r:gz') as tf, zipfile.ZipFile(
    zip_path, 'w', compression=zipfile.ZIP_DEFLATED
) as zf:
    for member in tf.getmembers():
        if not member.isfile():
            continue

        extracted = tf.extractfile(member)
        if extracted is None:
            continue

        data = extracted.read()
        zi = zipfile.ZipInfo(member.name)
        # Preserve unix permissions (best-effort)
        zi.external_attr = (member.mode & 0o777) << 16
        zf.writestr(zi, data)
PY
}

main() {
  if ! command -v git >/dev/null 2>&1; then
    exit 0
  fi

  local repo_root
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -z "$repo_root" ]]; then
    exit 0
  fi

  cd "$repo_root"

  local pyproject="${repo_root}/pyproject.toml"
  if [[ ! -f "$pyproject" ]]; then
    exit 0
  fi

  # Only consider commits that touched pyproject.toml
  if ! git show --name-only --pretty=format: HEAD | grep -qx "pyproject.toml"; then
    exit 0
  fi

  local new_version old_version
  new_version="$(get_version_from_pyproject "$pyproject")"

  old_version=""
  if git show HEAD^:pyproject.toml >/dev/null 2>&1; then
    old_version="$(git show HEAD^:pyproject.toml | get_version_from_pyproject_content || true)"
  fi

  if [[ -z "$old_version" ]]; then
    # No baseline to compare (e.g. first commit) -> do nothing.
    exit 0
  fi

  if [[ "$new_version" == "$old_version" ]]; then
    exit 0
  fi

  log "Detected version bump: ${old_version} -> ${new_version}"

  if ! python3 -m build --help >/dev/null 2>&1; then
    log "python3 -m build not available; skipping dist build"
    exit 0
  fi

  log "Building wheel + sdist into dist/"
  python3 -m build >/dev/null

  local sdist="dist/octoprint_tempeta-${new_version}.tar.gz"
  local zip="dist/octoprint_tempeta-${new_version}.zip"

  if [[ ! -f "$sdist" ]]; then
    log "Expected sdist not found: ${sdist}; skipping zip creation"
    exit 0
  fi

  log "Creating zip from sdist: ${zip}"
  rm -f "$zip"
  create_zip_from_sdist "$sdist" "$zip"

  log "Done: dist/ artifacts updated"
}

main "$@"
