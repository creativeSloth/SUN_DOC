import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy import create_engine

import files.logs_and_config as logs_and_config


def get_server_info(self):

    server = self.sett_con_dlg.ui.db_server.text()
    user = self.sett_con_dlg.ui.user.text()
    password = self.sett_con_dlg.ui.pw.text()
    dB_name = self.sett_con_dlg.ui.db_name.text()
    db_type = self.sett_con_dlg.ui.db_type.currentText()
    server_info = {
        "server": server,
        "user": user,
        "password": password,
        "dB_name": dB_name,
        "db_type": db_type,
    }
    return server_info


def execute_query(self, query):

    sql_query = get_sql_query(self)[query]

    # Konfiguriere MySQL-Verbindungsinformationen
    server_info = get_server_info(self)
    server = server_info["server"]
    user = server_info["user"]
    pw = server_info["password"]
    dB_name = server_info["dB_name"]
    db_type = server_info["db_type"]

    logs_and_config.update_config_file("Server", "server", server)
    logs_and_config.update_config_file("Server", "user", user)
    logs_and_config.update_config_file("Server", "password", pw)
    logs_and_config.update_config_file("Server", "dB_name", dB_name)
    try:

        if db_type == "MySQL":
            # Erstelle eine SQLAlchemy-Engine für MySQL-Verbindung
            engine = create_engine(
                f"mysql+mysqlconnector://{user}:{pw}@{server}/{dB_name}"
            )
            engine.connect()

        elif db_type == "PostgreSQL":
            # Erstelle eine SQLAlchemy-Engine für PostgreSQL-Verbindung
            engine = create_engine(
                f"postgresql+psycopg2://{user}:{pw}@{server}/{dB_name}"
            )
            engine.connect()

        else:
            # Fügen Sie hier weitere Datenbanktypen hinzu, wenn benötigt
            raise ValueError(f"Datenbanktyp wird nicht unterstützt: {db_type}")

        # Überprüfe, ob die Verbindung erfolgreich hergestellt wurde

        # Beispiel-SQL-Abfrage
        # if sql_query is None or sql_query == "":
        #     sql_query = "SELECT * FROM articles WHERE project_name = '{{project}}';"
        #     self.ui.query_input.setPlainText(sql_query)
        #     self.ui.query_2_input.setPlainText(sql_query)

        if "{{project}}" in sql_query:
            sql_query = sql_query.replace(
                "{{project}}", self.ui.project.toPlainText())

        # Verwende pd.read_sql, um die Abfrage auszuführen und die Ergebnisse in einen DataFrame zu lesen
        df = pd.read_sql(sql_query, con=engine)
        return df

    except Exception as e:
        # Gib eine Erfolgsmeldung aus
        QMessageBox.critical(
            self,
            "Verbindungsfehler zur Datenbank",
            f"Fehler bei der Verbindung zur Datenbank: {e}\n\n"
            "Überprüfen Sie die Zugangsinformationen zur SQL-Datenbank!",
        )
        return None


def get_sql_query(self):
    sql_query = {
        "sql1": self.sett_con_dlg.ui.query_input.toPlainText(),
        "sql2": self.sett_con_dlg.ui.query_2_input.toPlainText(),
    }
    return sql_query


def read_csv(file_path):
    # Lese CSV-Datei und gebe DataFrame zurück
    dtypes = {0: str, 1: str}
    df = pd.read_csv(file_path, header=None, dtype=dtypes)
    df = df.drop_duplicates()
    return df


def read_xlsx(file_path):
    # Lese Excel-Datei und gebe DataFrame zurück
    dtypes = {0: str, 1: str}
    df = pd.read_excel(file_path, header=None, dtype=dtypes)
    df = df.drop_duplicates()
    return df


def read_ods(file_path):
    # Lese Excel-Datei und gebe DataFrame zurück
    dtypes = {0: str, 1: str}
    df = pd.read_excel(file_path, header=None, dtype=dtypes, engine="odf")
    df = df.drop_duplicates()
    return df


def read_data_from_file(file_path):
    if file_path.endswith(".csv"):
        return read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return read_xlsx(file_path)
    elif file_path.endswith(".ods"):
        return read_ods(file_path)
