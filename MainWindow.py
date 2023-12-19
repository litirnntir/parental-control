import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QMessageBox, QDialog, QVBoxLayout
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtCore import QTimer, QThread
import time
from PyQt6.QtGui import QPalette, QBrush, QPixmap

from QMessages import incorrect_password
from system_functions import get_open_apps, close_app, get_active_app_name, send_notification
from settings import password, total_time
from SettingsWindow import SettingsWindow
import json
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # безрамочный интерфейс
        background_image = "background.png"
        pix = QPixmap(background_image)
        pal = QPalette()
        pal.setBrush(self.backgroundRole(), QBrush(pix))
        self.setPalette(pal)

        self.setObjectName("MainWindow")
        self.setFixedSize(840, 580)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.text_active_app = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_active_app.setGeometry(QtCore.QRect(70, 230, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(37)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.text_active_app.setFont(font)
        self.text_active_app.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.text_active_app.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   ")
        self.text_active_app.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.text_active_app.setObjectName("text_active_app")
        self.button_settings = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_settings.setGeometry(QtCore.QRect(70, 440, 331, 71))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        self.button_settings.setFont(font)
        self.button_settings.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   \n"
                                           "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(42, 146, 224, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_settings.setObjectName("button_settings")
        self.button_exit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_exit.setGeometry(QtCore.QRect(530, 380, 201, 101))

        self.button_settings.clicked.connect(self.openSettings)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.button_exit.setFont(font)
        self.button_exit.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border-radius: 20px;   \n"
                                       "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(21, 75, 115, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_exit.setObjectName("button_exit")
        self.button_add_time = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_add_time.setGeometry(QtCore.QRect(70, 340, 331, 71))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(23)
        self.button_add_time.setFont(font)
        self.button_add_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;   \n"
                                           "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.83, fx:0.5, fy:0.5, stop:0 rgba(42, 146, 224, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button_add_time.setObjectName("button_add_time")
        self.text_all_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.text_all_time.setGeometry(QtCore.QRect(70, 90, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(37)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.text_all_time.setFont(font)
        self.text_all_time.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.text_all_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border-radius: 20px;   ")
        self.text_all_time.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.text_all_time.setObjectName("text_all_time")
        self.time_all_time = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_all_time.setGeometry(QtCore.QRect(460, 80, 301, 91))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(55)
        self.time_all_time.setFont(font)
        self.time_all_time.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "border-color: rgb(255, 255, 255);\n"
                                         "border-radius: 20px;\n"
                                         "border: 2px solid;\n"
                                         "border-color: rgb(255, 255, 255);")
        self.time_all_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_all_time.setObjectName("time_all_time")
        self.time_active_app = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_active_app.setGeometry(QtCore.QRect(460, 210, 301, 91))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(55)
        self.time_active_app.setFont(font)
        self.time_active_app.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border-color: rgb(255, 255, 255);\n"
                                           "border-radius: 20px;\n"
                                           "border: 2px solid;\n"
                                           "border-color: rgb(255, 255, 255);")
        self.time_active_app.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_active_app.setObjectName("time_active_app")
        self.progress_bar_all_time = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_all_time.setGeometry(QtCore.QRect(460, 180, 301, 23))
        self.progress_bar_all_time.setProperty("value", 100)
        self.progress_bar_all_time.setTextVisible(True)
        self.progress_bar_all_time.setObjectName("progress_bar_all_time")
        self.progress_bar_active_app = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progress_bar_active_app.setGeometry(QtCore.QRect(460, 310, 301, 23))
        self.progress_bar_active_app.setStyleSheet("")
        self.progress_bar_active_app.setProperty("value", 100)
        self.progress_bar_active_app.setTextVisible(False)
        self.progress_bar_active_app.setObjectName("progress_bar_active_app")
        self.setCentralWidget(self.centralwidget)

        # self.blocked_apps = {'Notion': 60}
        # self.blocked_apps_for_percents = {'Notion': 60}  # На ноль секунд нельзя заблокировать

        self.stats_apps = {}
        # -----

        self.timer = QTimer()  # таймер
        self.timer.timeout.connect(self.update_data)  # подключаем сигнал таймера к слоту update_data
        self.timer.start(1000)  # таймер с интервалом в 1000 миллисекунд
        self.active_app = None

        self.time_left_block_app = 0  # Сколько времени осталось у заблокированного приложения
        self.time_spent = 0  # Времени проведено в приложении

        self.total_time = total_time  # секунд - хранение общего времени
        self.total_time_for_percents = total_time  # Переменная для создания бара
        self.password = password  # # для хранения пароля

        self.blocked_apps = self.get_blocked_apps_from_json()
        self.blocked_apps_for_percents = self.get_blocked_apps_for_percents_from_json()

        self.button_exit.clicked.connect(self.close)

        self.blocked_apps = self.get_blocked_apps_from_json()
        self.blocked_apps_for_percents = self.get_blocked_apps_for_percents_from_json()

        self.flag = True

        self.settings_window = None

        self.directory = None

        # -----

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Croak - Child Lock"))
        self.text_active_app.setText(_translate("MainWindow", "В активном приложении:"))
        self.button_settings.setText(_translate("MainWindow", "Настройки"))
        self.button_exit.setText(_translate("MainWindow", "Выйти"))
        self.button_add_time.setText(_translate("MainWindow", "Добавить время"))
        self.text_all_time.setText(_translate("MainWindow", "Осталось времени:"))
        self.time_all_time.setText(_translate("MainWindow", time.strftime("%H:%M:%S", time.gmtime(self.total_time))))
        self.time_active_app.setText(
            _translate("MainWindow", time.strftime("%H:%M:%S", time.gmtime(self.time_left_block_app))))

    def closeEvent(self, event):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Подтверждение выхода")
        dialog.setLabelText("Введите пароль:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

        ok = dialog.exec()
        password = dialog.textValue()

        with open("settings.json") as f:
            # Загружаем словарь с данными из файла
            data = json.load(f)
            # Присваиваем значения пароля и времени атрибутам self
            if ok and password == data["password"]:
                if self.settings_window:
                    self.settings_window.close()
                event.accept()
            else:
                incorrect_password()
                event.ignore()
        # Закрываем файл
        f.close()

    def get_blocked_apps_from_json(self):
        with open("blocked_apps.json", "r") as file:
            # Загружаем данные из файла в переменную data
            data = json.load(file)
        # Присваиваем переменную data словарю self.blocked_apps
        return data

    def get_blocked_apps_for_percents_from_json(self):
        with open("blocked_apps_for_percents.json", "r") as file:
            # Загружаем данные из файла в переменную data
            data = json.load(file)
        # Присваиваем переменную data словарю self.blocked_apps
        return data

    def openSettings(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Подтверждение выхода")
        dialog.setLabelText("Введите пароль:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

        ok = dialog.exec()
        password = dialog.textValue()

        with open("settings.json") as f:
            # Загружаем словарь с данными из файла
            data = json.load(f)
            # Присваиваем значения пароля и времени атрибутам self
            if ok and password == data["password"]:
                self.settings_window = SettingsWindow(self)
                # Показываем второе окно
                self.settings_window.show()
            else:
                incorrect_password()
        # Закрываем файл
        f.close()

    def update_settings(self):
        with open("settings.json") as f:
            data = json.load(f)
            self.password = data["password"]
            self.total_time = data["total_time"] * 60
            self.directory = data["directory"]
        f.close()

    def update_data(self):
        self.blocked_apps = self.get_blocked_apps_from_json()
        self.blocked_apps_for_percents = self.get_blocked_apps_for_percents_from_json()
        current_app = get_active_app_name()
        if self.total_time > 0 and self.flag:
            self.total_time -= 1
            if current_app != self.active_app:
                if self.time_spent > 1:
                    if self.active_app in self.stats_apps:
                        self.stats_apps[self.active_app] += self.time_spent
                    else:
                        self.stats_apps[self.active_app] = self.time_spent
                self.time_spent = 0
                if self.active_app in self.blocked_apps:
                    with open("blocked_apps.json", "r") as file:
                        # Загружаем данные из файла в переменную data
                        data = json.load(file)
                    # Обновляем или добавляем self.time_left_block_app в data с ключом self.active_app
                    data[self.active_app] = self.time_left_block_app
                    # Открываем файл blocked_apps.json в режиме записи
                    with open("blocked_apps.json", "w") as file:
                        # Записываем data в файл
                        json.dump(data, file)
                self.active_app = current_app
                if current_app in self.blocked_apps:
                    if self.blocked_apps[current_app] <= 1:
                        close_app(current_app)
                        self.time_left_block_app = 0

                        send_notification(f"Время {current_app} вышло. Вы больше не можете находиться в приложении")
                    else:
                        self.time_left_block_app = self.blocked_apps[current_app]
                        self.time_left_block_app -= 1
                else:
                    self.time_left_block_app = self.total_time
            else:
                self.time_spent += 1
                if current_app in self.blocked_apps:
                    if self.time_left_block_app <= 1:
                        close_app(current_app)
                        self.time_left_block_app = 0
                        send_notification(f"Время {current_app} вышло. Вы больше не можете находиться в приложении")

                        # QMessageBox.warning(self, f"Время {current_app} вышло",
                        #                     "Вы больше не можете находиться в приложении")
                    else:
                        self.time_left_block_app -= 1
                else:
                    self.time_left_block_app = self.total_time

            self.time_all_time.setText(time.strftime("%H:%M:%S", time.gmtime(self.total_time)))

            if self.time_left_block_app < self.total_time:
                self.time_active_app.setText(time.strftime("%H:%M:%S", time.gmtime(self.time_left_block_app)))
            else:
                self.time_active_app.setText(time.strftime("%H:%M:%S", time.gmtime(self.total_time)))

            if self.active_app in self.blocked_apps and self.time_left_block_app < self.total_time:
                if self.time_left_block_app > 1:
                    self.progress_bar_active_app.setProperty("value", 100 * self.time_left_block_app /
                                                             self.blocked_apps_for_percents[self.active_app])
                else:
                    self.progress_bar_active_app.setProperty("value", 0)
            else:
                self.progress_bar_active_app.setProperty("value",
                                                         100 * self.total_time / self.total_time_for_percents)
            self.progress_bar_all_time.setProperty("value", 100 * self.total_time / self.total_time_for_percents)
        elif self.total_time < 1 and self.flag:
            if current_app != "python" and current_app != "pycharm" and current_app != "Croak - Child Lock":
                close_app(current_app)
                apps_list = get_open_apps()
                if "pycharm" in apps_list: apps_list.remove("pycharm")
                if "python" in apps_list: apps_list.remove("python")
                if "Croak - Child Lock" in apps_list: apps_list.remove("Croak - Child Lock")
                if "Finder" in apps_list: apps_list.remove("Finder")
                for application in apps_list:
                    close_app(application)
        else:
            self.time_all_time.setText(time.strftime("%H:%M:%S", time.gmtime(0)))
            self.time_active_app.setText(time.strftime("%H:%M:%S", time.gmtime(0)))

            self.progress_bar_active_app.setProperty("value", 100)
            self.progress_bar_all_time.setProperty("value", 100)
        self.text_active_app.setText(f"В {self.active_app}:")
