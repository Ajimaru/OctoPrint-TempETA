# GitHub Workflows

This directory contains GitHub Actions workflows for automated testing and deployment.

## Available Workflows

### Build and Test (Planned)

- Runs on every push and pull request
- Tests code with pytest
- Runs pre-commit checks
- Checks code style with black, isort, and flake8

### Release (Planned)

- Automatic release creation
- PyPI package publishing

## Setting Up

To enable these workflows:

1. Push this repository to GitHub
2. Enable GitHub Actions in repository settings
3. Configure any necessary secrets (e.g., PyPI tokens for publishing)
