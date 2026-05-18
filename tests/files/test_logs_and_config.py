import configparser
import os

import pandas as pd
import pytest

import files.logs_and_config as lac
from directories.constants import (
    BLACKLISTS,
    CONFIG,
    DEVICE_SPECS,
    LOG_SUBF_2,
    SOURCE,
    TARGET_1,
)


def test_init_config_file_creates_file_with_expected_sections(tmp_path, reset_dirs):
    config_path = tmp_path / "config.ini"
    reset_dirs.paths[CONFIG] = str(config_path)

    lac.init_config_file()

    parser = configparser.ConfigParser()
    parser.read(config_path)
    assert parser.has_section("Pfade")
    assert parser.has_section("Abfrage")
    assert parser.has_section("Server")
    assert parser["Pfade"][SOURCE] == ""
    assert parser["Pfade"][CONFIG] == str(config_path)


def test_init_config_file_is_idempotent(tmp_path, reset_dirs):
    config_path = tmp_path / "config.ini"
    config_path.write_text("[Custom]\nfoo = bar\n")
    reset_dirs.paths[CONFIG] = str(config_path)

    lac.init_config_file()

    parser = configparser.ConfigParser()
    parser.read(config_path)
    assert parser.has_section("Custom")
    assert parser["Custom"]["foo"] == "bar"


def test_update_save_file_writes_field_map_into_section(tmp_path):
    save_file_path = tmp_path / "project.sav"
    save_file_path.write_text("[Fields text]\n[Tables content]\n")

    lac.update_save_file(
        field_map=[("project", "MRS 19-001"), ("notes", "hello")],
        file_path=str(save_file_path),
        section="Fields text",
    )

    parser = configparser.ConfigParser()
    parser.read(save_file_path)
    assert parser["Fields text"]["project"] == "MRS 19-001"
    assert parser["Fields text"]["notes"] == "hello"


def test_update_save_file_noops_on_empty_path(tmp_path):
    lac.update_save_file(field_map=[("a", "b")], file_path="", section="Fields text")
    # No exception, no side effects — only assertion is no crash.


def test_load_save_file_returns_empty_dict_when_section_missing(tmp_path):
    save_file_path = tmp_path / "empty.sav"
    save_file_path.write_text("[Other]\nkey = value\n")

    result = lac.load_save_file(str(save_file_path), "Fields text")
    assert result == {}


def test_load_save_file_returns_section_as_dict(tmp_path):
    save_file_path = tmp_path / "project.sav"
    save_file_path.write_text("[Fields text]\nproject = MRS\nnotes = abc\n")

    result = lac.load_save_file(str(save_file_path), "Fields text")
    assert result == {"project": "MRS", "notes": "abc"}


def test_roundtrip_update_then_load(tmp_path):
    save_file_path = tmp_path / "rt.sav"
    save_file_path.write_text("[Fields text]\n[Tables content]\n")

    field_map = [("a", "1"), ("b", "two")]
    lac.update_save_file(field_map=field_map, file_path=str(save_file_path),
                         section="Fields text")
    loaded = lac.load_save_file(str(save_file_path), "Fields text")
    assert loaded == {"a": "1", "b": "two"}


def test_update_config_file_then_read_back(tmp_path, reset_dirs):
    config_path = tmp_path / "config.ini"
    config_path.write_text("[Server]\nserver =\nuser =\n")
    reset_dirs.paths[CONFIG] = str(config_path)

    lac.update_config_file("Server", "user", "edgar")
    assert lac.read_config_value("Server", "user") == "edgar"


def test_change_str_to_config_format_replaces_special_chars():
    result = lac.change_str_to_config_format("[foo]\nbar")
    assert result == "<foo>bar"


def test_create_device_related_storage_list_creates_empty_file(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    lac.create_device_related_storage_list(storage_file=DEVICE_SPECS)
    assert file_path.exists()


def test_create_device_related_storage_list_is_idempotent(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    file_path.write_text("[Section]\nkey = preserve\n")
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    lac.create_device_related_storage_list(storage_file=DEVICE_SPECS)

    parser = configparser.ConfigParser()
    parser.read(file_path)
    assert parser["Section"]["key"] == "preserve"


def test_update_device_related_storage_list_writes_data_set(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    file_path.write_text("")
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    data_set = [("000001", "irrelevant", "module_power_kWp", "450")]
    lac.update_device_related_storage_list(DEVICE_SPECS, data_set)

    parser = configparser.ConfigParser()
    parser.read(file_path)
    assert parser.has_section("000001")
    assert parser["000001"]["module_power_kwp"] == "450"


def test_read_device_related_storage_list_returns_value(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    file_path.write_text("[000001]\nmodule_power_kwp = 450\n")
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    value = lac.read_device_related_storage_list(
        DEVICE_SPECS, "000001", "module_power_kWp"
    )
    assert value == "450"


def test_read_device_related_storage_list_returns_none_for_empty_value(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    file_path.write_text("[000001]\nmodule_power_kwp =\n")
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    assert (
        lac.read_device_related_storage_list(DEVICE_SPECS, "000001", "module_power_kWp")
        is None
    )


def test_read_device_related_storage_list_returns_none_for_missing_section(tmp_path, reset_dirs):
    file_path = tmp_path / "specs.ini"
    file_path.write_text("")
    reset_dirs.paths[DEVICE_SPECS] = str(file_path)

    assert (
        lac.read_device_related_storage_list(DEVICE_SPECS, "missing", "module_power_kWp")
        is None
    )


def test_log_copy_details_writes_log_with_expected_sections(tmp_path, reset_dirs):
    reset_dirs.paths[LOG_SUBF_2] = str(tmp_path)
    df = pd.DataFrame({"article_no": ["000001"], "article_name": ["A"]})

    lac.log_copy_details(
        self=None,
        source_path="/src",
        target_path="/tgt",
        source_files=["a.pdf", "b.pdf"],
        matching_files=["a.pdf"],
        df=df,
    )

    written = sorted(tmp_path.glob("datalog_*.txt"))
    assert len(written) == 1
    text = written[0].read_text(encoding="utf-8")
    assert "Source Folder: /src" in text
    assert "Target Folder: /tgt" in text
    assert "All Files in Source Folder:" in text
    assert "- a.pdf" in text
    assert "- b.pdf" in text
    assert "Selected documents:" in text
    assert "DataFrame from File or Database:" in text
    assert "article_no" in text
