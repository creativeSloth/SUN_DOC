import json
from configparser import ConfigParser
from unittest.mock import MagicMock

from ui.blacklists.storage_file_utils import (
    change_date_format,
    get_article_numbers_on_bl,
    get_data_of_articles_from_bl,
    is_on_blacklist,
)


def _make_table(object_name):
    table = MagicMock()
    table.objectName.return_value = object_name
    return table


def _write_blacklist(path, table_name, entries):
    parser = ConfigParser()
    parser.add_section(table_name)
    for key, entry in entries.items():
        parser.set(table_name, key, json.dumps(entry))
    with open(path, "w") as f:
        parser.write(f)


def test_is_on_blacklist_true_when_section_and_option_present():
    config = ConfigParser()
    config.add_section("articles_list")
    config.set("articles_list", "000001", "anything")
    assert is_on_blacklist("articles_list", "000001", config) is True


def test_is_on_blacklist_false_when_option_missing():
    config = ConfigParser()
    config.add_section("articles_list")
    assert is_on_blacklist("articles_list", "000001", config) is False


def test_is_on_blacklist_false_when_section_missing():
    config = ConfigParser()
    assert is_on_blacklist("articles_list", "000001", config) is False


def test_get_data_of_articles_from_bl_returns_parsed_entries(tmp_path, reset_dirs):
    from directories.constants import BLACKLISTS

    blacklist_path = tmp_path / "blacklists.ini"
    _write_blacklist(
        blacklist_path,
        "articles_list",
        {
            "000001": {
                "article_no": "000001",
                "article_name": "Modul",
                "date": "2024-01-02 - 03:04:05",
            }
        },
    )
    reset_dirs.paths[BLACKLISTS] = str(blacklist_path)

    result = get_data_of_articles_from_bl(table=_make_table("articles_list"))
    assert result == [("000001", "Modul", "2024-01-02 - 03:04:05")]


def test_get_data_of_articles_from_bl_returns_empty_when_section_absent(tmp_path, reset_dirs):
    from directories.constants import BLACKLISTS

    blacklist_path = tmp_path / "blacklists.ini"
    blacklist_path.write_text("")
    reset_dirs.paths[BLACKLISTS] = str(blacklist_path)

    assert get_data_of_articles_from_bl(table=_make_table("articles_list")) == []


def test_get_article_numbers_on_bl_delegates_to_get_data(tmp_path, reset_dirs):
    from directories.constants import BLACKLISTS

    blacklist_path = tmp_path / "blacklists.ini"
    _write_blacklist(
        blacklist_path,
        "modules_list",
        {
            "000016": {
                "article_no": "000016",
                "article_name": "PV-Modul",
                "date": "2024-05-01 - 12:00:00",
            }
        },
    )
    reset_dirs.paths[BLACKLISTS] = str(blacklist_path)

    result = get_article_numbers_on_bl(table=_make_table("modules_list"))
    assert result == [("000016", "PV-Modul", "2024-05-01 - 12:00:00")]


def test_change_date_format_normalises_separators_and_colons():
    entry = ("000001", "Modul", "2024-01-02 - 03:04:05")
    assert change_date_format(entry) == "2024-01-02_03-04-05"
