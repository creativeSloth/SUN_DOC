import pandas as pd
import pytest

from source.data_origins import (
    read_csv,
    read_data_from_file,
    read_ods,
    read_xlsx,
)


def _write_csv(path, rows):
    path.write_text("\n".join(",".join(r) for r in rows))


def test_read_csv_returns_dataframe_with_string_dtype(tmp_path):
    csv = tmp_path / "data.csv"
    _write_csv(csv, [["000001", "Modul"], ["000002", "Wechselrichter"]])

    df = read_csv(str(csv))

    assert list(df[0]) == ["000001", "000002"]
    assert df[0].dtype == object
    assert df[1].dtype == object


def test_read_csv_drops_duplicates(tmp_path):
    csv = tmp_path / "data.csv"
    _write_csv(csv, [["000001", "A"], ["000001", "A"], ["000002", "B"]])

    df = read_csv(str(csv))
    assert len(df) == 2


def test_read_xlsx_reads_two_columns_as_strings(tmp_path):
    xlsx = tmp_path / "data.xlsx"
    pd.DataFrame([["000001", "Modul"], ["000002", "Inv"]]).to_excel(
        xlsx, header=False, index=False
    )

    df = read_xlsx(str(xlsx))
    assert df.iloc[0, 0] == "000001"
    assert df[0].dtype == object


def test_read_ods_reads_two_columns(tmp_path):
    ods = tmp_path / "data.ods"
    pd.DataFrame([["000001", "Modul"]]).to_excel(
        ods, header=False, index=False, engine="odf"
    )

    df = read_ods(str(ods))
    assert df.iloc[0, 0] == "000001"


def test_read_data_from_file_dispatches_on_extension_csv(tmp_path):
    csv = tmp_path / "x.csv"
    _write_csv(csv, [["000001", "A"]])
    df = read_data_from_file(str(csv))
    assert df.iloc[0, 0] == "000001"


def test_read_data_from_file_dispatches_on_extension_xlsx(tmp_path):
    xlsx = tmp_path / "x.xlsx"
    pd.DataFrame([["000001", "A"]]).to_excel(xlsx, header=False, index=False)
    df = read_data_from_file(str(xlsx))
    assert df.iloc[0, 0] == "000001"


def test_read_data_from_file_returns_none_for_unsupported_extension(tmp_path):
    other = tmp_path / "x.txt"
    other.write_text("000001,A")
    assert read_data_from_file(str(other)) is None
