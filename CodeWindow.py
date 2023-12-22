import sys
import json
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTime


class CodeWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Введите код")
        self.resize(300, 100)
        self.code_edit = QtWidgets.QLineEdit(self)
        self.code_edit.setPlaceholderText("Введите код здесь")
        self.confirm_button = QtWidgets.QPushButton("Подтвердить", self)
        self.confirm_button.clicked.connect(self.check_code)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.code_edit)
        self.layout.addWidget(self.confirm_button)

    def update_total_time(self, value):
        with open("settings.json", "r+") as f:
            data = json.load(f)
            data["total_time"] = data["total_time"] + value
            f.seek(0)
            f.truncate()
            json.dump(data, f)
        f.close()
        self.main_window.update_settings()

    def update_time_app(self, value, app):
        with open("blocked_apps.json", "r+") as f:
            data = json.load(f)
            data[app] = data[app] + value
            f.seek(0)
            f.truncate()
            json.dump(data, f)
        with open("blocked_apps_for_percents.json", "r+") as f:
            data = json.load(f)
            data[app] = data[app] + value
            f.seek(0)
            f.truncate()
            json.dump(data, f)
        f.close()

    def check_code(self):
        code = self.code_edit.text()
        codes = {}
        with open("code.json", "r") as f:
            codes = json.load(f)
        if code in codes:
            print(codes[code]["Приложение"], codes[code]["Время"])
            if codes[code]["Приложение"] == "total":
                with open("settings.json") as f:
                    self.update_total_time(codes[code]["Время"])
                    # Удаление из кодов
                    codes.pop(code)
                    with open("code.json", "w") as f:
                        json.dump(codes, f)
            else:
                with open("blocked_apps.json") as f:
                    blocked =json.load(f)
                    if codes[code]["Приложение" in blocked]:
                        self.update_time_app(codes[code]["Время"], code)
                        # Удаление из кодов
                        codes.pop(code)
                        with open("code.json", "w") as f:
                            json.dump(codes, f)
                    else:
                         QtWidgets.QMessageBox.warning(self, "Ошибка", f'Приложение {codes[code]["Приложение"]} не заблокировано')

            with open("blocked_apps.json", "w") as f:
                json.dump(codes, f)

            QtWidgets.QMessageBox.information(self, "Успешно", "Код верный")

        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Код неверный")

        self.close()
