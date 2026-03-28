from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QApplication, QVBoxLayout
from basewindow import BaseWindow

class SettingsWindow(BaseWindow):
    def __init__(self):
        super().__init__("Settings Window")
        self.setMinimumSize(0, 0)
        self.table = None
        self.data: list

        layout = QVBoxLayout()
        self.header = QHBoxLayout()
        self.main = QVBoxLayout()
        self.footer = QHBoxLayout()

        self.init_header()
        self.init_main()
        self.init_footer()

        layout.addLayout(self.header)
        layout.addLayout(self.main)
        layout.addLayout(self.footer)

        self.setLayout(layout)
        self.load_settings()

    def init_header(self):
        self.checkbox_ext_db = QCheckBox("External database")

        self.checkbox_int_db =  QCheckBox("Internal database")
        self.checkbox_int_db.setChecked(True)

        self.header.addWidget(self.checkbox_ext_db)
        self.header.addWidget(self.checkbox_int_db)

    def init_main(self):
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host address")

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port number")

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")

        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("Database name")

        self.main.addWidget(self.host_input)
        self.main.addWidget(self.port_input)
        self.main.addWidget(self.user_input)
        self.main.addWidget(self.password_input)
        self.main.addWidget(self.db_name_input)

    def init_footer(self):
        self.save_settings_btn = QPushButton("Save settings")

        self.footer.addWidget(self.save_settings_btn)
