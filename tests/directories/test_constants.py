import pytest

from directories.constants import DIRS, SOURCE, Paths


def test_paths_initialises_all_known_keys_to_empty_string():
    paths = Paths()
    assert paths.paths[SOURCE] == ""
    assert all(value == "" for value in paths.paths.values())


def test_set_path_normalises_backslashes_to_forward_slashes():
    paths = Paths()
    paths.set_path(SOURCE, r"C:\some\windows\path")
    assert paths.get_path(SOURCE) == "C:/some/windows/path"


def test_set_path_raises_on_unknown_key():
    paths = Paths()
    with pytest.raises(KeyError):
        paths.set_path("not_a_real_key", "/tmp")


def test_get_path_raises_on_unknown_key():
    paths = Paths()
    with pytest.raises(KeyError):
        paths.get_path("not_a_real_key")


def test_module_level_DIRS_is_a_Paths_instance():
    assert isinstance(DIRS, Paths)
