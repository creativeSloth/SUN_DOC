from types import SimpleNamespace

from database.queries import get_query_for_articles_on_table


def test_get_query_for_articles_on_table_contains_expected_fragments():
    self = SimpleNamespace()
    self.ui = SimpleNamespace(articles_list=object())
    self.GENERAL_TABLE_MAP = {
        self.ui.articles_list: {"db_bl_bool": "on_articles_bl"},
    }

    query = get_query_for_articles_on_table(
        self, bool_arg="on_modules_bl", date_arg="added_to_modules_bl"
    )

    assert "FROM" in query
    assert "INNER JOIN" in query
    assert "articles" in query
    assert "blacklists" in query
    assert "on_modules_bl" in query
    assert "added_to_modules_bl" in query
    # Falls back to the general articles_list flag in the OR clause.
    assert "on_articles_bl" in query
