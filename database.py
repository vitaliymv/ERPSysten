import sqlite3
from PyQt5.QtCore import QSettings

class Database:
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.settings = QSettings("Robocode", "RobocodeErpSystem")
        self.is_internal = self.settings.value("internal_db", True, bool)

    def __enter__(self):
        self.connect_cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def connect_cursor(self):
        if self.is_internal:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row