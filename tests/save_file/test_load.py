from unittest.mock import MagicMock

from save_file.load import fill_field_value


def test_fill_field_value_sets_text_when_field_name_in_map():
    field = MagicMock()
    field.objectName.return_value = "Project"
    saved = {"project": "MRS 19-001"}

    fill_field_value(field, saved)

    field.setPlainText.assert_called_once_with("MRS 19-001")


def test_fill_field_value_uses_lowercase_field_name_as_lookup_key():
    field = MagicMock()
    field.objectName.return_value = "NOTES"
    saved = {"notes": "abc"}

    fill_field_value(field, saved)

    field.setPlainText.assert_called_once_with("abc")


def test_fill_field_value_skips_when_field_name_not_in_map():
    field = MagicMock()
    field.objectName.return_value = "absent"
    saved = {"other": "x"}

    fill_field_value(field, saved)

    field.setPlainText.assert_not_called()
