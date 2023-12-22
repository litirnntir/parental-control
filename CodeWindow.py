import sys
import json
from PyQt6 import QtWidgets, QtGui


class CodeWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите код")
        self.resize(300, 100)
        self.code_edit = QtWidgets.QLineEdit(self)
        self.code_edit.setPlaceholderText("Введите код здесь")
        self.confirm_button = QtWidgets.QPushButton("Подтвердить", self)
        self.confirm_button.clicked.connect(self.check_code)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.code_edit)
        self.layout.addWidget(self.confirm_button)

    def check_code(self):
        code = self.code_edit.text()
        with open("code.json", "r") as f:
            codes = json.load(f)
        if code in codes:
            QtWidgets.QMessageBox.information(self, "Успешно", "Код верный")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Код неверный")
