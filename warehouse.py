from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets
from basewindow import BaseWindow
from database import WarehouseTable

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
        self.delete_btn.clicked.connect(self.delete_item)

        self.edit_item_btn = QPushButton("Edit item")
        self.edit_item_btn.setObjectName("items-button")
        self.edit_item_btn.clicked.connect(self.edit_item)

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

        with WarehouseTable() as wt:
            self.data = wt.get_items()
            self.table.setRowCount(len(self.data))

            for row, item in enumerate(self.data):
                item = dict(item)
                item.pop("id")
                for col, val in enumerate(item.values()):
                    t_item = QTableWidgetItem(str(val))
                    self.table.setItem(row, col, t_item)

        self.content_layout.addWidget(self.table)

    def add_item(self):
        inputs = self.show_edit_window("Add item", "Name", "Price", "Description", "Category")
        if not inputs:
            return

        for i in inputs:
            if not i.strip():
                self.show_modal("Error", "One of the inputs are empty", 1)
                return

        with WarehouseTable() as wt:
            wt.add_item(*inputs)

        self.show_table()

    def get_table_item_id(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        item_values = []
        for i in range(self.table.columnCount()):
            item_values.append(self.table.item(selected_row, i).text())

        selected_id = None
        for item in self.data:
            current_item = dict(item)
            current_item = list(current_item.values())[1:]
            current_item = [str(i) for i in current_item]
            if current_item == item_values:
                selected_id = dict(item)["id"]

        return selected_id, item_values

    def delete_item(self):
        selected_id = self.get_table_item_id()
        if selected_id is None:
            self.show_modal("Warning", "No item selected", 1)
            return

        with WarehouseTable() as wt:
            wt.remove_item(int(selected_id[0]))
        self.show_table()

    def edit_item(self):
        item_obj = self.get_table_item_id()
        if item_obj is None:
            self.show_modal("Warning", "No item selected", 1)
            return
        selected_id = item_obj[0]

        inputs = self.show_edit_window("Edit item", "Name", "Price", "Description", "Category", values=item_obj[1])

        if not inputs:
            return

        for i in inputs:
            if not i.strip():
                self.show_modal("Error", "One of the inputs are empty", 1)
                return

        with WarehouseTable() as wt:
            wt.update_item(int(selected_id), *inputs)

        self.show_table()
