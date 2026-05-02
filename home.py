from datetime import datetime
from basewindow import BaseWindow
from database import OrderTable, JobTable, WarehouseTable
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollArea, QListWidget, QVBoxLayout, QSpinBox, QLineEdit, \
    QHBoxLayout, QListWidgetItem, QDialog, QMessageBox, QWidget
from PyQt5.QtCore import Qt

class HomePageWindow(BaseWindow):
    def __init__(self):
        super().__init__("Home")
        self.setMinimumSize(0, 0)
        layout = QVBoxLayout()

        self.header_layout = QVBoxLayout()
        self.init_header()

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.show_order_details)

        layout.addLayout(self.header_layout)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def init_header(self):
        header_label = QLabel("ERP System")
        header_label.setObjectName("home_header_page")

        header_btn = QPushButton("Add new order")
        header_btn.setObjectName("home_page_header_button")

        self.header_layout.addWidget(header_label, alignment=Qt.AlignCenter)
        self.header_layout.addWidget(header_btn)

    def show_orders(self):
        self.list_widget.clear()
        with OrderTable() as ot:
            self.orders_data = ot.get_orders()
            seen_ids = set()
            for o in self.orders_data:
                order_id = o["order_id"]
                if order_id in seen_ids:
                    continue
                seen_ids.add(order_id)
                text = f"{o['customer_name']} | {o['status']} | {o['created_at']}"
                item = QListWidgetItem(text)
                item.setData(Qt.UserRole, o['order_id'])
                self.list_widget.addItem(item)

    def show_order_details(self, item):
        order_id = item.data(Qt.UserRole)

        details = [o for o in self.orders_data if o["order_id"] == order_id]
        if not details:
            return
        order = details[0]

        text = f"Order #{order_id}\n"
        text += f"Customer name: {order['customer_name']}\n"
        text += f"Status: {order['status']}\n"
        text += f"Date: {order['created_at']}\n\n"

        text += "📋 Jobs: \n"
        job_lines = set()
        for d in details:
            if d['job_id']:
                line = f"- {d['job_name']} ({d['job_quantity']} pcs, {d['job_price'] * d['job_quantity']} $)"
                job_lines.add(line)

        text += "\n".join(job_lines) if job_lines else "Empty"

        text += "\n\n📦 Parts: "
        item_lines = set()
        for d in details:
            if d['item_id']:
                line = f"- {d['item_name']} ({d['item_quantity']} pcs, {d['item_price'] * d['item_quantity']} $)"
                item_lines.add(line)

        text += "\n".join(item_lines) if item_lines else "Empty"

        text += f"\n\nDetails: {order['notes']}"
        QMessageBox.information(self, f"Order {order_id}", text)

    def show_order_window(self):
        window = QDialog()
        window.setWindowTitle("Add order")
        window.setModal(True)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.customer_name_field = QLineEdit()
        self.customer_name_field.setPlaceholderText("Customer name")

        self.notes_field = QLineEdit()
        self.notes_field.setPlaceholderText("Notes about order")

        with JobTable() as jt:
            all_jobs = jt.get_job()
        with WarehouseTable() as wt:
            all_parts = wt.get_items()

        orders_data = {
            "job": [],
            "item": []
        }

        def create_list(item_list, name):
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)

            for item in item_list:
                row = QHBoxLayout()
                label = QLabel(f"{item['id']}." + item[f"{name}_name"])
                label.setMinimumWidth(100)
                spin = QSpinBox()
                spin.setMinimum(0)
                spin.setMaximum(100)
                spin.setFixedWidth(50)

                row.addWidget(label)
                row.addStretch()
                row.addWidget(QLabel("q-ty."))
                row.addWidget(spin)

                scroll_layout.addLayout(row)
                orders_data[name].append((item["id"], spin))

            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            scroll_area.setMaximumHeight(200)
            scroll_area.setMinimumWidth(300)
            return scroll_area

        items_layout = QHBoxLayout()
        items_layout.addWidget(create_list(all_jobs, "job"))
        items_layout.addWidget(create_list(all_parts, "item"))

        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(window.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(window.reject)
        button_layout.addWidget(cancel_button)

        layout.addWidget(self.customer_name_field)
        layout.addWidget(self.notes_field)
        layout.addLayout(items_layout)
        layout.addLayout(button_layout)
        window.setLayout(layout)
        return window, orders_data

    def add_order(self):
        window, orders_data = self.show_order_window()
        result = window.exec_()
        if not result:
            return
        jobs = orders_data["job"]
        parts = orders_data["item"]

        filtered_jobs = [
            {
                "id": job_id,
                "quantity": int(spinbox.text())
            }
            for job_id, spinbox in jobs if int(spinbox) > 0
        ]

        filtered_parts = [
            {
                "id": part_id,
                "quantity": int(spinbox.text())
            }
            for part_id, spinbox in parts if int(spinbox) > 0
        ]

        now = datetime.now()
        now_str = now.strftime("%A(%d) %B %Y, %H:%M")
        with OrderTable() as ot:
            ot.create_order(
                self.customer_name_field.text(),
                now_str,
                "In progress",
                self.notes_field.text(),
                filtered_jobs,
                filtered_parts
            )
            self.show_orders()
