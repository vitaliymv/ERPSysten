from PyQt5.QtWidgets import QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QApplication, QVBoxLayout
from basewindow import BaseWindow

class SettingsWindow(BaseWindow):
    def __init__(self):
        super().__init__("Settings Window")
        self.setMinimumSize(0, 0)

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
        self.checkbox_ext_db.clicked.connect(self.set_external_db)
        self.checkbox_int_db =  QCheckBox("Internal database")
        self.checkbox_int_db.clicked.connect(self.set_internal_db)

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
        self.save_settings_btn.clicked.connect(self.save_settings)
        self.footer.addWidget(self.save_settings_btn)

    def set_external_db(self):
        self.checkbox_ext_db.setEnabled(False)
        self.checkbox_ext_db.setChecked(True)
        self.checkbox_int_db.setEnabled(True)
        self.checkbox_int_db.setChecked(False)

        for i in range(self.main.count()):
            self.main.itemAt(i).widget().setEnabled(True)

    def set_internal_db(self):
        self.checkbox_ext_db.setEnabled(True)
        self.checkbox_ext_db.setChecked(False)
        self.checkbox_int_db.setEnabled(False)
        self.checkbox_int_db.setChecked(True)

        for i in range(self.main.count()):
            self.main.itemAt(i).widget().setEnabled(False)

    def save_settings(self):
        self.settings.setValue("internal_db", self.checkbox_int_db.isChecked())
        self.settings.setValue("external_db", self.checkbox_ext_db.isChecked())
        for i in range(self.main.count()):
            widget = self.main.itemAt(i).widget()
            field_name = widget.placeholderText()
            field_name = field_name.replace(" ", "").lower()
            if widget.text():
                if "port" in field_name:
                    self.settings.setValue(field_name, str(widget.text()))
                else:
                    self.settings.setValue(field_name, widget.text())
        QApplication.quit()

    def load_settings(self):
        is_internal = self.settings.value("internal_db", True, bool)
        is_external = self.settings.value("external_db", False, bool)
        if is_internal:
            self.set_internal_db()
        if is_external:
            self.set_external_db()

        self.host_input.setText(self.settings.value("hostaddress", "localhost", str))
        self.port_input.setText(str(self.settings.value("portnumber", 5432, int)))
        self.user_input.setText(self.settings.value("username", "admin", str))
        self.password_input.setText(self.settings.value("password", "qweqwe", str))
        self.db_name_input.setText(self.settings.value("databasename", "erp", str))