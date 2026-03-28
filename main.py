from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from basewindow import BaseWindow, Drawer
from dataclasses import dataclass
import sys
from settings import SettingsWindow

class BusinessERP(BaseWindow):
    def __init__(self):
        super().__init__("Robocode ERP system")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.drawer_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.content_layout.addWidget(QLabel("Main block"))
        self.settings_page_window = SettingsWindow()
        self.drawer = Drawer()
        self.init_drawer()
        self.drawer_layout.addWidget(self.drawer.widget)

        main_layout.addLayout(self.drawer_layout)
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

    def init_drawer(self):
        @dataclass
        class DrawerButton:
            widget: QPushButton
            open_icon: str
            close_icon: str

        home_page_btn = QPushButton("Home")
        home_page_btn.setObjectName("drawer_button")
        home_page_btn_widget = DrawerButton(home_page_btn, "🏠 Home", "🏠")

        warehouse_page_btn = QPushButton("Warehouse")
        warehouse_page_btn.setObjectName("drawer_button")
        warehouse_page_btn_widget = DrawerButton(warehouse_page_btn, "📦 Warehouse", "📦")

        jobs_page_btn = QPushButton("Jobs")
        jobs_page_btn.setObjectName("drawer_button")
        jobs_page_btn_widget = DrawerButton(jobs_page_btn, "📋 Jobs", "📋")

        settings_page_btn = QPushButton("Settings")
        settings_page_btn.setObjectName("drawer_button")
        settings_page_btn_widget = DrawerButton(settings_page_btn, "⚙️ Settings", "⚙️")
        # settings_page_btn.clicked.connect()

        quit_page_btn = QPushButton("Quit")
        quit_page_btn.setObjectName("drawer_button")
        quit_page_btn_widget = DrawerButton(quit_page_btn, "❌ Quit", "❌")

        self.drawer.init_layout(
            home_page_btn_widget,
            warehouse_page_btn_widget,
            jobs_page_btn_widget,
            settings_page_btn_widget,
            quit_page_btn_widget
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusinessERP()
    window.show()
    sys.exit(app.exec_())