# Development scripts

This folder contains helper scripts for local development.

None of these scripts contain hardcoded, machine-specific absolute paths. Wherever a path is needed, it is either auto-discovered (repo-relative) or configurable via environment variables.

## Quick start

```bash
# from repo root
.development/setup_dev.sh
```

## Scripts

### setup_dev.sh

Creates/uses a local Python virtual environment in `./venv`, installs the plugin in editable mode with dev dependencies, and enables the repo-local git hooks.

```bash
.development/setup_dev.sh
```

Notes:

- It automatically sets `git config core.hooksPath .githooks` (if the repo is a git checkout).
- `pre-commit` is optional: if it is not installed, it will be skipped with a warning.

### restart_octoprint_dev.sh

Stops OctoPrint (by default: the instance listening on `OCTOPRINT_PORT`), optionally clears webassets cache, and starts OctoPrint again.

```bash
# basic restart
.development/restart_octoprint_dev.sh

# restart and clear OctoPrint webassets cache (useful after frontend changes)
.development/restart_octoprint_dev.sh --clear-cache

# stop all detected OctoPrint instances for the current user before restarting
.development/restart_octoprint_dev.sh --stop-all

# show help
.development/restart_octoprint_dev.sh --help
```

Configuration (environment variables):

- `OCTOPRINT_CMD=/path/to/octoprint` (preferred)
- `OCTOPRINT_VENV=/path/to/venv` (uses `$OCTOPRINT_VENV/bin/octoprint`)
- `OCTOPRINT_PORT=5000`
- `OCTOPRINT_ARGS="serve --debug"`
- `OCTOPRINT_BASEDIR=$HOME/.octoprint`
- `OCTOPRINT_LOG=$OCTOPRINT_BASEDIR/logs/octoprint.log`
- `NOHUP_OUT=/tmp/octoprint.nohup`

How `octoprint` is resolved (in order):

1. `OCTOPRINT_CMD`
2. `OCTOPRINT_VENV/bin/octoprint`
3. repo-relative fallbacks (e.g. `./venv/bin/octoprint`)
4. `octoprint` on `PATH`

### post_commit_build_dist.sh

Builds fresh distribution artifacts into `dist/` after a commit **only when the project version changed** in `pyproject.toml` compared to the previous commit.

- Creates wheel + sdist via `python3 -m build`
- Creates an additional `.zip` (derived from the sdist `.tar.gz`) for convenience

You usually don't run this manually. It is called by the git `post-commit` hook.

### test_checklist.sh

Prints a human-readable quick checklist (versions, file presence, rough counts). It does **not** run automated tests.

```bash
.development/test_checklist.sh
```

## Git hooks

The repo uses a versioned hooks directory:

- Hook path: `.githooks/`
- Enabled via: `git config core.hooksPath .githooks`

The `post-commit` hook triggers `post_commit_build_dist.sh` after version bumps.
