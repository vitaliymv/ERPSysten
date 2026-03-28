from PyQt5.QtCore import QSettings, Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton


class BaseWindow(QWidget):
    def __init__(self, header: str) -> None:
        super().__init__()
        self.setWindowTitle(header)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(700, 400)
        self.settings = QSettings("Robocode", "RobocodeErpSystem")

    def show_modal(self, header: str, text: str, icon: int = 0):
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(text)
        match icon:
            case 0: msg.setIcon(QMessageBox.Information)
            case 1: msg.setIcon(QMessageBox.Warning)
            case 2: msg.setIcon(QMessageBox.Critical)
            case 3: msg.setIcon(QMessageBox.Question)
            case _: raise Exception("Enter valid icon number")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def show_edit_window(header: str, *fields, values=None):
        window = QDialog()
        window.setWindowTitle(header)
        window.setModal(True)

        layout = QVBoxLayout()
        inputs = []
        for i, button in enumerate(fields):
            layout.addWidget(QLabel(button))
            if values is not None:
                edit_input = QLineEdit(values[i])
            else:
                edit_input = QLineEdit()
            inputs.append(edit_input)
            layout.addWidget(edit_input)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(window.accept)
        button_layout.addWidget(ok_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(window.reject)
        button_layout.addWidget(cancel_btn)

        window.setLayout(button_layout)
        if window.exec_() == QDialog.Accepted:
            return [i.text() for i in inputs]
        else:
            return False

class Drawer:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("drawer-wrapper")
        self.drawer_layout = QVBoxLayout()
        self.button_size = 50
        self.widget.setMaximumWidth(self.button_size * 4)
        self.widget.setMinimumWidth(self.button_size)
        self.object_widgets = None
        self.animation = None
        self.is_moving = False

    def init_layout(self, *widgets):
        self.drawer_layout.setContentsMargins(0, 0, 0, 0)
        self.drawer_layout.setSpacing(0)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(self.button_size, self.button_size)
        self.toggle_btn.setObjectName("toggle_drawer_button")
        self.toggle_btn.clicked.connect(self.toggle_drawer)

        self.drawer_layout.addWidget(self.toggle_btn, alignment=Qt.AlignLeft)
        self.drawer_layout.setAlignment(Qt.AlignTop)

        self.object_widgets = widgets
        for w in self.object_widgets:
            t_widget = w.widget
            t_widget.setFixedHeight(self.button_size)
            self.drawer_layout.addWidget(t_widget, alignment=Qt.AlignTop)

        self.widget.setLayout(self.drawer_layout)
        self.toggle_drawer()

    def toggle_drawer(self):
        if self.is_moving:
            return

        def on_animation_finished():
            self.is_moving = False

        self.widget.animation = QPropertyAnimation(self.widget, b"maximumWidth")
        self.widget.animation.setDuration(500)
        self.widget.animation.finished.connect(on_animation_finished)

        self.is_moving = True
        if self.widget.width() == self.button_size:
            self.widget.animation.setStartValue(self.button_size)
            self.widget.animation.setEndValue(self.button_size * 4)
            self.toggle_btn.setText("X")
            for widget in self.object_widgets:
                widget.widget.setText(widget.open_icon)
        else:
            self.widget.animation.setStartValue(self.button_size * 4)
            self.widget.animation.setEndValue(self.button_size)
            self.toggle_btn.setText("☰")
            for widget in self.object_widgets:
                widget.widget.setText(widget.close_icon)

        self.widget.animation.start()