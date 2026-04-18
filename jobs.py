from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets
from basewindow import BaseWindow
from database import JobTable
from PyQt5.QtCore import QDate

class JobWindow(BaseWindow):
    def __init__(self):
        super().__init__("Job Window")
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
        self.add_job_btn = QPushButton("Add job")
        self.add_job_btn.setObjectName("jobs-button")
        self.add_job_btn.clicked.connect(self.add_job)

        self.delete_btn = QPushButton("Delete job")
        self.delete_btn.setObjectName("jobs-button")
        self.delete_btn.clicked.connect(self.delete_job)

        self.edit_job_btn = QPushButton("Edit job")
        self.edit_job_btn.setObjectName("jobs-button")
        self.edit_job_btn.clicked.connect(self.edit_job)

        self.header_layout.addWidget(self.add_job_btn)
        self.header_layout.addWidget(self.delete_btn)
        self.header_layout.addWidget(self.edit_job_btn)

    def show_table(self):
        if self.table:
            self.content_layout.removeWidget(self.table)
            self.table.setParent(None)
            self.table.deleteLater()

        self.table = QTableWidget()
        self.table.setMaximumSize(700, 400)
        self.table.setColumnCount(5)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Description", "Category", "Estimate time"])

        with JobTable() as jt:
            self.data = jt.get_job()
            self.table.setRowCount(len(self.data))

            for row, job in enumerate(self.data):
                job = dict(job)
                job.pop("id")
                for col, val in enumerate(job.values()):
                    t_job = QTableWidgetItem(str(val))
                    self.table.setItem(row, col, t_job)

        self.content_layout.addWidget(self.table)

    def add_job(self):
        inputs = self.show_edit_window("Add job", "Name", "Price", "Description", "Category", "Estimate time")
        if not inputs:
            return

        for i in inputs:
            if not i.strip():
                self.show_modal("Error", "One of the inputs are empty", 1)
                return

        with JobTable() as wt:
            wt.add_job(*inputs)

        self.show_table()

    def get_table_job_id(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        job_values = []
        for i in range(self.table.columnCount()):
            job_values.append(self.table.item(selected_row, i).text())

        selected_id = None
        for job in self.data:
            current_job = dict(job)
            current_job = list(current_job.values())[1:]
            current_job = [str(i) for i in current_job]
            if current_job == job_values:
                selected_id = dict(job)["id"]

        return selected_id, job_values

    def delete_job(self):
        selected_id = self.get_table_job_id()
        if selected_id is None:
            self.show_modal("Warning", "No job selected", 1)
            return

        with JobTable() as jt:
            jt.remove_job(int(selected_id[0]))
        self.show_table()

    def edit_job(self):
        job_obj = self.get_table_job_id()
        if job_obj is None:
            self.show_modal("Warning", "No job selected", 1)
            return

        selected_id = job_obj[0]
        inputs = self.show_edit_window("Edit job", "Name", "Price", "Description", "Category", "Estimate time", values=job_obj[1])

        if not inputs:
            return

        for i in inputs:
            if not i.strip():
                self.show_modal("Error", "One of the inputs are empty", 1)
                return

        with JobTable() as jt:
            jt.update_job(int(selected_id), *inputs)

        self.show_table()
