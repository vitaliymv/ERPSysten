import sqlite3
from PyQt5.QtCore import QSettings

class Database:
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.settings = QSettings("Robocode", "RobocodeErpSystem")
        self.is_internal = self.settings.value("internal_db", True, bool)
        self.is_internal = True
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

class JobTable(Database):
    def __init__(self, db_name: str = "database.db"):
        super().__init__(db_name)
        self.table = """
            CREATE TABLE IF NOT EXISTS job (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name VARCHAR(50) NOT NULL,
                job_price DOUBLE NOT NULL,
                description TEXT NOT NULL,
                est_time VARCHAR(255) NOT NULL,
                category VARCHAR(50) NOT NULL
            )
        """

    def get_job(self):
        self.cursor.execute("SELECT * FROM job")
        return self.cursor.fetchall()

    def remove_job(self, job_id: int):
        self.cursor.execute("DELETE FROM job WHERE id = ?", (job_id, ))

    def add_job(self, job_name, job_price, description, est_time, category):
        self.cursor.execute(
            "INSERT INTO job (job_name, job_price, description, est_time, category) VALUES (?, ?, ?, ?, ?)",
            (job_name, job_price, description, est_time, category)
        )

    def update_job(self, job_id, job_name, job_price, description, est_time, category):
        self.cursor.execute(
            "UPDATE job SET job_name = ?, job_price = ?, description = ?, est_time = ?, category = ? WHERE id = ?",
            (job_name, job_price, description, est_time, category, job_id)
        )

class OrderTable(Database):
    def __init__(self, db_name: str = "database.db"):
        super().__init__(db_name)
        self.table = """
            CREATE TABLE IF NOT EXISTS order (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name VARCHAR(100) NOT NULL,
                created_at TEXT NOT NULL,
                status VARCHAR(20) NOT NULL,
                notes TEXT NOT NULL
            )
        """

    def create_sub_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1
            )
        """)

    def create_order(self, customer_name, created_at, status, notes, jobs, parts):
        self.create_sub_tables()
        self.cursor.execute(
            "INSERT INTO order (customer_name, created_at, status, notes) VALUES (?, ?, ?, ?)",
            (customer_name, created_at, status, notes)
        )

        order_id = self.cursor.lastrowid
        for j in jobs:
            self.cursor.execute(
                "INSERT INTO orders_jobs (order_id, job_id, quantity) VALUES (?, ?, ?)",
                (order_id, j["id"], j["quantity"])
            )

        for p in parts:
            self.cursor.execute(
                "INSERT INTO orders_parts (order_id, part_id, quantity) VALUES (?, ?, ?)",
                (order_id, p["id"], p["quantity"])
            )

        return order_id

    def get_orders_basic(self):
        self.create_sub_tables()
        self.cursor.execute("SELECT * FROM order")
        return self.cursor.fetchall()

    def get_orders(self):
        self.create_sub_tables()
        self.cursor.execute("""
            SELECT o.id AS order_id, o.customer_name, o.created_at, o.status, o.notes, 
            oj.job_id, oj.quantity AS job_quantity, j.job_name, j.job_price, j.description AS job_description,
            j.est_time, j.category AS job_category, op.part_id AS item_id, w.item_name, w.item_price, 
            w.description AS item_description, w.category AS item_category, op.quantity AS item_quantity 
            FROM order o 
            LEFT JOIN orders_jobs oj ON o.id = oj.order_id 
            LEFT JOIN job j ON j.id = oj.job_id 
            LEFT JOIN orders_parts op ON o.id = op.order_id 
            LEFT JOIN warehouse w ON op.part_id = w.id ORDER BY o.id
        """)
        return self.cursor.fetchall()

#