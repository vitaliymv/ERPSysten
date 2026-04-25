from datetime import datetime
from basewindow import BaseWindow
from database import OrderTable, JobTable, WarehouseTable
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollArea, QListWidget, QVBoxLayout, QSpinBox, QLineEdit, \
    QHBoxLayout, QListWidgetItem, QDialog, QMessageBox
from PyQt5.QtCore import Qt

class HomePageWindow(BaseWindow):
    def __init__(self):
        super().__init__("Home")
        self.setMinimumSize(0, 0)
        layout = QVBoxLayout()

        self.header_layout = QVBoxLayout()
        self.init_header()

        self.list_widget = QListWidget()

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