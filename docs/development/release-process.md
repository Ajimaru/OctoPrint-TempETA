# Release Process

This document describes the release process for OctoPrint-TempETA.

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes
- **PRERELEASE**: `rc1`, `rc2`, `beta1`, `alpha1`

Examples:

- `0.7.0` - Minor release
- `0.7.1` - Patch release
- `0.8.0rc1` - Release candidate
- `1.0.0` - Major release

## Release Checklist

### 1. Prepare Release

- [ ] All target issues/PRs are merged
- [ ] All tests pass on CI
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] No known critical bugs

### 2. Version Bump

Update version in:

1. `pyproject.toml`:
   ```toml
   version = "0.8.0"
   ```

2. `octoprint_temp_eta/__init__.py`:
   ```python
   __version__ = "0.8.0"
   ```

3. `package.json` (if changed):
   ```json
   "version": "0.8.0"
   ```

### 3. Update CHANGELOG

Add release notes to `CHANGELOG.md`:

```markdown
## [0.8.0] - 2024-01-15

### Added
- Exponential ETA algorithm
- MQTT retain option
- German translations

### Changed
- Improved ETA accuracy near target
- Updated UI for better contrast

### Fixed
- ETA calculation for cooling
- MQTT reconnection logic

### Deprecated
- Old settings format (migration automatic)

### Removed
- Python 3.10 support

### Security
- Updated paho-mqtt to address CVE-XXXX-XXXX
```

### 4. Create Release Branch

```bash
git checkout -b release/v0.8.0
git add pyproject.toml octoprint_temp_eta/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.8.0"
git push origin release/v0.8.0
```

### 5. Open Release PR

Create PR from `release/v0.8.0` to `main`:

- Title: "Release v0.8.0"
- Description: Copy changelog section
- Wait for CI to pass
- Get review approval

### 6. Merge Release PR

Merge the release PR to `main`.

### 7. Create Git Tag

```bash
git checkout main
git pull
git tag -a v0.8.0 -m "Release v0.8.0"
git push origin v0.8.0
```

### 8. Create GitHub Release

Go to [Releases](https://github.com/Ajimaru/OctoPrint-TempETA/releases) → "Draft a new release"

- Tag: `v0.8.0`
- Title: `OctoPrint-TempETA v0.8.0`
- Description: Copy from CHANGELOG
- Attach build artifacts (auto-generated)
- Check "Set as latest release"
- Publish

### 9. Verify Release

- [ ] GitHub release is created
- [ ] GitHub Actions completed successfully
- [ ] Release assets are available
- [ ] Documentation is deployed
- [ ] PyPI package is available (if published)

### 10. Announce Release

- Update README if needed
- Post in OctoPrint community
- Update plugin repository listing

## Hotfix Process

For critical bugs in production:

### 1. Create Hotfix Branch

```bash
git checkout main
git checkout -b hotfix/v0.7.1
```

### 2. Fix and Test

- Fix the bug
- Add regression test
- Verify fix works

### 3. Version Bump

Update to patch version (e.g., `0.7.0` → `0.7.1`)

### 4. Release

Follow normal release process starting from step 5.

## Pre-release Process

For release candidates and betas:

### 1. Create Pre-release

```bash
git checkout -b release/v0.8.0rc1
# Update version to "0.8.0rc1"
git commit -m "Bump version to 0.8.0rc1"
git push
```

### 2. Tag Pre-release

```bash
git tag -a v0.8.0rc1 -m "Release candidate 1 for v0.8.0"
git push origin v0.8.0rc1
```

### 3. GitHub Pre-release

Create GitHub release:

- Check "This is a pre-release"
- Description mentions it's not stable
- Users can test before final release

### 4. Test Pre-release

- Get feedback from testers
- Fix reported issues
- Create rc2, rc3 as needed

### 5. Final Release

When ready, release as `v0.8.0` (without rc suffix)

## Automated Release

The project uses GitHub Actions for automated releases:

`.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

## Release Assets

Each release includes:

- **Source tarball**: `OctoPrint-TempETA-0.8.0.tar.gz`
- **Wheel**: `OctoPrint_TempETA-0.8.0-py3-none-any.whl`
- **Release notes**: Extracted from CHANGELOG

## PyPI Release (Optional)

If publishing to PyPI:

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Verify installation
pip install --index-url https://test.pypi.org/simple/ OctoPrint-TempETA

# Upload to PyPI
twine upload dist/*
```

## Documentation Release

Documentation is automatically deployed on release:

1. Tag triggers docs workflow
2. MkDocs builds site
3. Deployed to GitHub Pages
4. Available at https://ajimaru.github.io/OctoPrint-TempETA/

## Post-Release Tasks

### 1. Update Development Version

After release, bump to next development version:

```python
# In pyproject.toml
version = "0.9.0dev"
```

### 2. Create Milestone

Create GitHub milestone for next release:

- Title: `v0.9.0`
- Due date: Estimated release date
- Move unfinished issues to new milestone

### 3. Update Project Board

- Close current milestone
- Archive completed items
- Plan next release

## Rollback Process

If critical issue found after release:

### 1. Assess Impact

- How many users affected?
- Severity of issue?
- Can users downgrade?

### 2. Options

**Option A: Immediate Hotfix**

- Create hotfix branch
- Fix and release patch version
- Announce fix available

**Option B: Rollback Release**

- Delete GitHub release (if just released)
- Delete git tag
- Fix issue
- Re-release with same version

**Option C: Yanked Release**

- Mark release as broken
- Recommend users downgrade
- Fix in next release

### 3. Communication

- Update GitHub release with warning
- Post in issues/discussions
- Email users if contact available

## Version Support

- **Latest release**: Full support
- **Previous minor**: Security fixes only
- **Older versions**: No support

## Breaking Changes

When introducing breaking changes:

1. **Deprecate first**: Mark old API as deprecated
2. **Document migration**: Provide upgrade guide
3. **Major version bump**: Increment MAJOR version
4. **Announce early**: Warn users in advance

Example:

```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

## Release Calendar

Typical release schedule:

- **Patch releases**: As needed (bug fixes)
- **Minor releases**: Every 2-3 months (features)
- **Major releases**: Yearly (breaking changes)

## Security Releases

For security issues:

1. **Don't publicize**: Fix privately
2. **Create patch**: Minimal fix
3. **Release ASAP**: Same day if possible
4. **Backport**: Apply to supported versions
5. **Announce**: After fix is available

See [SECURITY.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/SECURITY.md) for details.

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Highlights

Brief overview of major changes.

### Added
- New feature 1
- New feature 2

### Changed
- Improvement 1
- Improvement 2

### Fixed
- Bug fix 1
- Bug fix 2

### Deprecated
- Old API 1 (use X instead)

### Removed
- Dropped support for Python 3.10

### Security
- Fixed vulnerability CVE-XXXX-XXXX

### Upgrade Notes

Special instructions for upgrading.

### Contributors

Thanks to @user1, @user2, @user3
```

## Automation Tools

Tools used in release process:

- **GitHub Actions**: CI/CD
- **pytest**: Testing
- **build**: Package building
- **twine**: PyPI uploads
- **MkDocs**: Documentation
- **pre-commit**: Code quality

## Release FAQ

**Q: Can I release without tests passing?**
A: No, all tests must pass before release.

**Q: What if I find a bug after tagging?**
A: Delete the tag, fix the bug, and re-tag. If already on GitHub, release a patch.

**Q: How do I test a release before publishing?**
A: Use pre-release tags (rc1, rc2) and mark as pre-release on GitHub.

**Q: Can I change a released version?**
A: No, released versions are immutable. Release a new patch version.

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute
- [Testing Guide](testing.md) - Testing before release
- [CHANGELOG](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/CHANGELOG.md) - Release history
