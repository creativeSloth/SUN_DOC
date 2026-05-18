"""Test configuration: sys.path, headless Qt, and shared fixtures."""
import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(scope="session")
def qapp():
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def reset_dirs():
    """Reset the global DIRS singleton between tests that mutate it."""
    from directories.constants import DIRS

    original = dict(DIRS.paths)
    yield DIRS
    DIRS.paths = original
