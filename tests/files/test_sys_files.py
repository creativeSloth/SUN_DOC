import os

from files.sys_files import (
    get_files_in_directory,
    get_matching_files,
    itter_through_sub_directories,
)


def test_get_matching_files_returns_substring_matches():
    source = ["000001_A.pdf", "000002_B.pdf", "noise.txt"]
    selected = ["000001", "000003"]
    assert get_matching_files(source, selected) == ["000001_A.pdf"]


def test_get_matching_files_empty_selection_returns_empty():
    assert get_matching_files(["x.pdf"], []) == []


def test_get_matching_files_matches_substring_anywhere_in_name():
    # Confirms documented behaviour: any substring counts.
    source = ["report_000005_v1.pdf"]
    assert get_matching_files(source, ["000005"]) == ["report_000005_v1.pdf"]


def test_itter_through_sub_directories_walks_recursively(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "root.pdf").write_text("x")
    (tmp_path / "sub" / "nested.pdf").write_text("y")

    files = itter_through_sub_directories(self=None, directory=str(tmp_path))

    # Paths are returned relative to `directory`.
    assert sorted(files) == sorted(["root.pdf", os.path.join("sub", "nested.pdf")])


def test_get_files_in_directory_returns_relative_files(tmp_path):
    (tmp_path / "a.pdf").write_text("x")
    (tmp_path / "b.docx").write_text("y")

    files = get_files_in_directory(self=None, directory=str(tmp_path))
    assert sorted(files) == ["a.pdf", "b.docx"]


def test_get_files_in_directory_returns_empty_for_empty_dir(tmp_path):
    assert get_files_in_directory(self=None, directory=str(tmp_path)) == []
