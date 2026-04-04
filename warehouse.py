from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets
from basewindow import BaseWindow

class WarehouseWindow(BaseWindow):
    def __init__(self):
        super().__init__("Warehouse Window")
        self.setMinimumSize(0, 0)

        layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.content_layout = QVBoxLayout()

        self.table = None
        self.data: list

        self.init_header()
        self.show_table()

        layout.addLayout(self.header_layout)
        layout.addLayout(self.content_layout)

        self.setLayout(layout)


    def init_header(self):
        self.add_item_btn = QPushButton("Add item")
        self.add_item_btn.setObjectName("items-button")
        self.add_item_btn.clicked.connect(self.add_item)

        self.delete_btn = QPushButton("Delete item")
        self.delete_btn.setObjectName("items-button")

        self.edit_item_btn = QPushButton("Edit item")
        self.edit_item_btn.setObjectName("items-button")

        self.header_layout.addWidget(self.add_item_btn)
        self.header_layout.addWidget(self.delete_btn)
        self.header_layout.addWidget(self.edit_item_btn)

    def show_table(self):
        if self.table:
            self.content_layout.removeWidget(self.table)
            self.table.setParent(None)
            self.table.deleteLater()

        self.table = QTableWidget()
        self.table.setMaximumSize(700, 400)
        self.table.setColumnCount(4)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Description", "Category"])

        self.content_layout.addWidget(self.table)

    def add_item(self):
        inputs = self.show_edit_window("Add item", "Name", "Price", "Description", "Category")
        if not inputs:
            return

        for i in inputs:
            if not i.strip():
                self.show_modal("Error", "One of the inputs are empty", 1)
                return

        self.show_table()