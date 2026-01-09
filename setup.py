# coding=utf-8

"""Setuptools compatibility shim.

The primary build configuration lives in pyproject.toml.

We keep this setup.py for legacy/fallback tooling and to provide a small build-time
hook that ensures compiled translation catalogs are packaged reliably.
"""

import os
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


def _sync_translations() -> None:
    """Sync top-level translations into the package directory.

    Wheels include package data, but do not include arbitrary top-level folders.
    To make i18n robust, we keep a copy of the translation catalogs under
    octoprint_temp_eta/translations and refresh it automatically during builds.
    """

    repo_root = os.path.dirname(os.path.abspath(__file__))
    src_root = os.path.join(repo_root, "translations")
    dst_root = os.path.join(repo_root, "octoprint_temp_eta", "translations")

    if not os.path.isdir(src_root):
        return

    os.makedirs(dst_root, exist_ok=True)

    # Remove known generated subfolders to avoid stale files lingering.
    for sub in ("de", "en"):
        p = os.path.join(dst_root, sub)
        if os.path.isdir(p):
            shutil.rmtree(p)

    # Copy tree (Python 3.7 compatible: no dirs_exist_ok in copytree).
    for root, _dirs, files in os.walk(src_root):
        rel = os.path.relpath(root, src_root)
        target_dir = dst_root if rel == os.curdir else os.path.join(dst_root, rel)
        os.makedirs(target_dir, exist_ok=True)
        for name in files:
            src_file = os.path.join(root, name)
            dst_file = os.path.join(target_dir, name)
            shutil.copy2(src_file, dst_file)


class build_py(_build_py):

    def run(self) -> None:
        _sync_translations()
        super().run()


class sdist(_sdist):

    def run(self) -> None:
        _sync_translations()
        super().run()


setup(
    cmdclass={
        "build_py": build_py,
        "sdist": sdist,
    }
)
