import re

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from database.utils import create_session, get_db_engine, set_val_by_mode


def test_set_val_by_mode_add_without_date_returns_true_and_timestamp():
    on_bl, date = set_val_by_mode("add", None)

    assert on_bl is True
    assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", date)


def test_set_val_by_mode_add_with_date_preserves_date():
    on_bl, date = set_val_by_mode("add", "2024-01-02_03-04-05")

    assert on_bl is True
    assert date == "2024-01-02_03-04-05"


def test_set_val_by_mode_remove_returns_false_and_none():
    on_bl, date = set_val_by_mode("remove", "ignored")

    assert on_bl is False
    assert date is None


def test_get_db_engine_uses_DIRS_DB_path(tmp_path, reset_dirs):
    from directories.constants import DB

    db_path = tmp_path / "test.db"
    reset_dirs.paths[DB] = str(db_path)

    engine = get_db_engine()
    assert isinstance(engine, Engine)
    assert str(db_path) in str(engine.url)


def test_create_session_returns_open_session(tmp_path, reset_dirs):
    from directories.constants import DB

    reset_dirs.paths[DB] = str(tmp_path / "test.db")

    session = create_session()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()
