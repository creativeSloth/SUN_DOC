import os
import sys
import types

import pytest

import directories.directories_handler as handler
from directories.constants import (
    BLACKLISTS,
    CONFIG,
    DB,
    DEVICE_SPECS,
    ICONS_FOLDER,
    LOG_SUBF,
    LOG_SUBF_2,
    STYLESHEET,
)


@pytest.fixture
def fake_main_module(tmp_path, monkeypatch):
    """Pretend that main.py lives in tmp_path so handler resolves paths there."""
    main_path = tmp_path / "main.py"
    main_path.write_text("# fake main")

    fake_main = types.ModuleType("__main__")
    fake_main.__file__ = str(main_path)
    monkeypatch.setitem(sys.modules, "__main__", fake_main)
    monkeypatch.setattr(sys, "frozen", False, raising=False)
    return tmp_path


def test_get_main_dir_returns_directory_of_main(fake_main_module):
    assert handler.get_main_dir() == str(fake_main_module)


def test_make_subfolders_creates_both_directories(tmp_path):
    logs = tmp_path / "logs"
    hist = logs / "hist"
    handler.make_subfolders(str(logs), str(hist))
    assert logs.is_dir()
    assert hist.is_dir()


def test_create_name_of_files_builds_expected_paths(fake_main_module):
    log_dir = str(fake_main_module / "logs")
    (
        config_path,
        blacklist_path,
        db_path,
        device_specs_path,
        stylesheet_path,
        icons_folder_path,
    ) = handler.create_name_of_files(log_dir)

    assert os.path.dirname(config_path) == log_dir
    assert config_path.endswith("config.ini")
    assert blacklist_path.endswith("blacklists.ini")
    assert db_path.endswith("SUN_DOC_DB.db")
    assert device_specs_path.endswith("device_specs_list.ini")
    assert stylesheet_path.endswith(os.path.join("styles", "stylesheet.qss"))
    assert icons_folder_path.endswith(os.path.join("ui", "icons"))


def test_set_static_directories_populates_DIRS(fake_main_module, reset_dirs):
    handler.set_static_directories()

    for key in (LOG_SUBF, LOG_SUBF_2, CONFIG, BLACKLISTS, DB,
                DEVICE_SPECS, STYLESHEET, ICONS_FOLDER):
        assert reset_dirs.paths[key] != ""
        assert "\\" not in reset_dirs.paths[key]

    assert os.path.isdir(reset_dirs.paths[LOG_SUBF])
    assert os.path.isdir(reset_dirs.paths[LOG_SUBF_2])
