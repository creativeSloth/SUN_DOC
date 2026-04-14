from typing import Any, Dict, Set

import pandas as pd
from sqlalchemy.orm import Session
from PyQt5.QtWidgets import QTableWidget
from sqlalchemy import Engine, Column
from sqlalchemy.exc import SQLAlchemyError

from database.classes import Article, ArticleSpecifications, Blacklists
from database.constants import (
    COLUMN_ARTICLE_NAME,
    COLUMN_ARTICLE_NO,
    DB_TABLE_NAME_ARTICLES,
    DB_TABLE_NAME_BLACKLISTS,
)
from database.utils import create_session, get_db_engine, set_val_by_mode
from ui.tables.constants import SPEC_DB_MAP


def get_query_for_articles_on_table(self, bool_arg, date_arg):
    bl_bool_article_list = self.GENERAL_TABLE_MAP[self.ui.articles_list]["db_bl_bool"]

    return f"""
    SELECT 
        {DB_TABLE_NAME_ARTICLES}.{COLUMN_ARTICLE_NAME},
        {DB_TABLE_NAME_ARTICLES}.{COLUMN_ARTICLE_NO},
        {DB_TABLE_NAME_BLACKLISTS}.{bool_arg},
        {DB_TABLE_NAME_BLACKLISTS}.{date_arg}
    FROM 
        {DB_TABLE_NAME_ARTICLES}
    INNER JOIN 
        {DB_TABLE_NAME_BLACKLISTS} 
    ON 
        {DB_TABLE_NAME_ARTICLES}.id = {DB_TABLE_NAME_BLACKLISTS}.article_id
    WHERE
        {DB_TABLE_NAME_BLACKLISTS}.{bool_arg} = TRUE 
    OR    
        {DB_TABLE_NAME_BLACKLISTS}.{bl_bool_article_list} = TRUE
    """


def update_db_blacklist(
    self,
    article_no: str,
    article_name: str,
    table: QTableWidget,
    mode: str = "add",
    date: str = None,
) -> None:
    """
    Aktualisiert die Blacklists-Tabelle in der blacklist.db.

    :param article_no: Artikelnummer
    :param article_name: Artikelname
    :param table: QTableWidget
    :param mode: Modus ("add" oder "remove")
        "add" Fügt den Artikel zur DB-Tabelle hinzu, fals er noch nicht vorhanden ist. Falls doch, werden die Werte (*_val)
        in den Spalten entsprechend der Argumente "bl_bool_arg" und "bl_date_arg" bestimmt und gesetzt
        "remove": Der Artikel bleibt in der DB erhalten. Die Werte werden in den Spalten
        entsprechend der Argumente "bl_bool_arg" und "bl_date_arg" auf False (bl_bool_val) bzw. auf None (bl_date_val) gesetzt.

        Die Modus-Entscheidung erfolgt in einer Hilfsfunktion "set_val_by_mode(mode)"

    :return: None
    """

    bl_bool_arg = self.GENERAL_TABLE_MAP[table]["db_bl_bool"]
    bl_date_arg = self.GENERAL_TABLE_MAP[table]["db_added_to_bl_date"]

    session: Session = create_session()

    try:

        bl_bool_val, bl_date_val = set_val_by_mode(mode, date)

        blacklist_change: dict = {
            bl_bool_arg: bl_bool_val,
            bl_date_arg: bl_date_val,
        }

        # Überprüfen, ob article_no bereits in der Blacklists-Tabelle existiert
        existing_article_entry = (
            session.query(Article).filter_by(article_no=article_no).first()
        )

        if existing_article_entry:
            existing_blacklist_entry = (
                session.query(Blacklists)
                .filter_by(article_id=existing_article_entry.id)
                .first()
            )

            if existing_blacklist_entry is None:
                commit_new_joined_list_entry(
                    db_object=Blacklists,
                    session=session,
                    secondary_id=Blacklists.article_id,
                    db_join_object=existing_article_entry,
                    **blacklist_change,
                )
            else:
                setattr(existing_blacklist_entry, bl_bool_arg, bl_bool_val)
                setattr(existing_blacklist_entry, bl_date_arg, bl_date_val)
                set_general_bl_to_none(self, mode, existing_blacklist_entry)

                session.commit()

        else:
            new_article_entry = commit_new_entry_and_return(
                db_object=Article,
                session=session,
                article_no=article_no,
                article_name=article_name,
            )

            commit_new_joined_list_entry(
                db_object=Blacklists,
                session=session,
                secondary_id=Blacklists.article_id,
                db_join_object=new_article_entry,
                **blacklist_change,
            )

    except SQLAlchemyError as e:
        if session:
            session.rollback()
        raise e
    finally:
        session.close()


def set_general_bl_to_none(self, mode, existing_entry):

    if mode == "remove":

        # Setzt die Werte in den allgemeinen Artikelspalten, da
        # die Blacklist-Werte für dieses Artikel gelöscht werden sollen.
        # Diese Änderungen werden in den allgemeinen Artikelspalten gespeichert.

        bl_bool_general: bool = self.GENERAL_TABLE_MAP[self.ui.articles_list][
            "db_bl_bool"
        ]
        bl_date_general: str = self.GENERAL_TABLE_MAP[self.ui.articles_list][
            "db_added_to_bl_date"
        ]

        setattr(existing_entry, bl_bool_general, False)
        setattr(existing_entry, bl_date_general, None)


def get_value_from_db_art_specs_list(article_no: str, column_header: str) -> str:
    """Es wird anhand einer Artikelnummer und einer Spaltenbezeichnung, welche aus einem QTableWidget erhalten wurden,
    ein Eintrag aus einer Tabelle einer Datenbank gelesen. Der Wert des EItnrags wird zurück gegegeben.
    :param article_no: Artikelnummer
    :param column_header: Spaltenbezeichnung
    :return: Wert des Eintrags oder None, falls der Eintrag nicht gefunden wurde"""

    article_specs_arg: str = SPEC_DB_MAP[column_header]
    if article_specs_arg is None:
        raise ValueError(f"ungültige Spaltenbezeichnung: {column_header}")

    session: Session = create_session()
    try:
        existing_article_entry: Article = (
            session.query(Article).filter_by(article_no=article_no).first()
        )
        if not existing_article_entry:
            return None
        existing_spec_list_entry = (
            session.query(ArticleSpecifications)
            .filter_by(article_id=existing_article_entry.id)
            .first()
        )
        if not existing_spec_list_entry:
            return None
        return getattr(existing_spec_list_entry, article_specs_arg, None)

    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_db_article_spec_list(data_set: Set[tuple]) -> None:
    """
    Aktualisiert die Artikelspezifikations-Tabelle in der SUN-DOC.db.
    :param data_set: Set mit Artikelnummer, Artikelname, Spezifikation und Wert
    :return: None
    """
    try:
        for article_no, article_name, spec, article_specs_val in data_set:

            session: Session = create_session()
            article_specs_arg: str = SPEC_DB_MAP[spec]

            article_specs_change: Dict[str, Any] = {
                article_specs_arg: article_specs_val,
            }

            # Überprüfen, ob article_no bereits in der Blacklists-Tabelle existiert
            existing_article_entry: Article = (
                session.query(Article).filter_by(article_no=article_no).first()
            )

            if existing_article_entry:

                existing_spec_list_entry = (
                    session.query(ArticleSpecifications)
                    .filter_by(article_id=existing_article_entry.id)
                    .first()
                )
                if existing_spec_list_entry is None:
                    commit_new_joined_list_entry(
                        db_object=ArticleSpecifications,
                        session=session,
                        secondary_id=ArticleSpecifications.article_id,
                        db_join_object=existing_article_entry,
                        **article_specs_change,
                    )
                else:
                    setattr(
                        existing_spec_list_entry, article_specs_arg, article_specs_val
                    )
                    session.commit()

            else:

                new_article_entry = commit_new_entry_and_return(
                    db_object=Article,
                    session=session,
                    article_no=article_no,
                    article_name=article_name,
                )

                commit_new_joined_list_entry(
                    db_object=ArticleSpecifications,
                    session=session,
                    secondary_id=ArticleSpecifications.article_id,
                    db_join_object=new_article_entry,
                    **article_specs_change,
                )

    except SQLAlchemyError as e:
        if session:
            session.rollback()
        raise e
    finally:
        session.close()


def commit_new_joined_list_entry(
    db_object: Any,
    session: Session,
    secondary_id: Column,
    db_join_object: Column,
    **kwargs: Any,
) -> None:
    """
    Führt eine Eintrag in einer Beziehungstabelle aus.
    :param db_object: Die zu verwendende Beziehungstabelle
    :param session: Die Datenbank-Session
    :param secondary_id: Die Spalte, in der die Beziehung eingerichtet wird
    :param db_join_object: Die Spalte, in der der Bezug hergestellt wird
    :param kwargs: Die Attribute des Eintrags

    :return: None
    """
    kwargs[secondary_id.name] = db_join_object.id
    new_spec_list_entry = db_object(**kwargs)
    session.add(new_spec_list_entry)
    session.commit()


def commit_new_entry_and_return(db_object: Any, session: Session, **kwargs: Any) -> Any:
    """
    Führt eine EIntrag in einer bestimmten Datenbanktable aus.
    :param db_object: Die zu verwendende Datenbanktabelle
    :param session: Die Datenbank-Session
    :param kwargs: Die Attribute des Eintrags
    :return: Das neu erstellte Eintrag"""

    new_entry = db_object(**kwargs)
    session.add(new_entry)
    session.commit()
    return new_entry


def get_bl_df_from_db(self, table: QTableWidget):

    bl_bool_arg = self.GENERAL_TABLE_MAP[table]["db_bl_bool"]
    bl_date_arg = self.GENERAL_TABLE_MAP[table]["db_added_to_bl_date"]

    # Definiere die SQL-Abfrage, um nur bestimmte Spalten auszuwählen
    engine: Engine = get_db_engine()
    query: str = get_query_for_articles_on_table(
        self, bl_bool_arg, bl_date_arg)
    # Lese die Tabelle direkt in einen DataFrame
    bl_df: pd.DataFrame = pd.DataFrame()
    bl_df = pd.read_sql_query(query, con=engine)

    bl_df[bl_date_arg] = bl_df[bl_date_arg].fillna(
        "Auf allgemeiner Blackliste")

    return bl_df
