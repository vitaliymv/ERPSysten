import sqlite3
from PyQt5.QtCore import QSettings

class Database:
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.settings = QSettings("Robocode", "RobocodeErpSystem")
        self.is_internal = self.settings.value("internal_db", True, bool)
        self.table = None

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

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(self.table)
        except:
            return

class WarehouseTable(Database):
    def __init__(self, db_name: str = "database.db"):
        super().__init__(db_name)
        self.table = """
            CREATE TABLE IF NOT EXISTS warehouse (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name VARCHAR(50) NOT NULL,
                item_price DOUBLE NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50) NOT NULL
            )                
        """

    def get_items(self):
        self.cursor.execute("SELECT * FROM warehouse")
        return self.cursor.fetchall()

    def remove_item(self, item_id: int):
        self.cursor.execute("DELETE FROM warehouse WHERE id = ?", (item_id, ))

    def add_item(self, item_name: str, item_price: float, description: str, category: str):
        self.cursor.execute(
            "INSERT INTO warehouse (item_name, item_price, description, category) VALUES (?, ?, ?, ?)",
            (item_name, item_price, description, category)
        )

    def update_item(self, item_id: int, item_name: str, item_price: float, description: str, category: str):
        self.cursor.execute("""
            UPDATE warehouse SET item_name = ?, item_price = ?, description = ?, category = ? WHERE id = ?
        """, (item_name, item_price, description, category, item_id))