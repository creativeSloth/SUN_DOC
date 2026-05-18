import pytest
from sqlalchemy import inspect

from database.classes import Article, ArticleSpecifications, Blacklists, init_local_db
from database.constants import (
    DB_TABLE_NAME_ART_SPECS,
    DB_TABLE_NAME_ARTICLES,
    DB_TABLE_NAME_BLACKLISTS,
)
from database.utils import get_db_engine


@pytest.fixture
def db_in_tmp(tmp_path, reset_dirs):
    from directories.constants import DB

    reset_dirs.paths[DB] = str(tmp_path / "test.db")
    return reset_dirs.paths[DB]


def test_init_local_db_creates_all_three_tables(db_in_tmp):
    init_local_db()

    engine = get_db_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert DB_TABLE_NAME_ARTICLES in tables
    assert DB_TABLE_NAME_BLACKLISTS in tables
    assert DB_TABLE_NAME_ART_SPECS in tables


def test_article_model_metadata():
    assert Article.__tablename__ == DB_TABLE_NAME_ARTICLES
    columns = {c.name for c in Article.__table__.columns}
    assert {"id", "article_no", "article_name"} <= columns


def test_blacklists_model_has_expected_boolean_columns():
    columns = {c.name for c in Blacklists.__table__.columns}
    for expected in (
        "on_articles_bl",
        "on_modules_bl",
        "on_pv_inv_bl",
        "on_bat_inv_bl",
        "on_bat_bl",
        "on_chg_point_bl",
    ):
        assert expected in columns


def test_article_specifications_has_expected_columns():
    columns = {c.name for c in ArticleSpecifications.__table__.columns}
    for expected in (
        "module_power_kWp",
        "inv_power_kW",
        "bat_inv_power_kW",
        "coupling_type",
        "bat_capacity_kWh",
        "max_discharge_power_kW",
        "bat_technology_type",
    ):
        assert expected in columns


def test_insert_article_via_orm_persists(db_in_tmp):
    from database.utils import create_session

    init_local_db()
    session = create_session()
    try:
        session.add(Article(article_no="000001", article_name="Modul"))
        session.commit()

        result = session.query(Article).filter_by(article_no="000001").one()
        assert result.article_name == "Modul"
    finally:
        session.close()
