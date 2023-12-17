import signal

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog
from PyQt6.QtCore import QTimer, Qt
import time
from PyQt6.QtGui import QPalette, QBrush, QPixmap, QFont
import os


# Определяем функцию, которая принимает название приложения в качестве аргумента
def close_app(app_name):
    try:
        processes = os.popen("ps ax").readlines()
        for process in processes:
            if app_name in process:
                fields = process.split()
                pid = fields[0]
                os.kill(int(pid), signal.SIGTERM)
                print(f"Закрыли приложение {app_name}")
    except:
        pass


def get_open_apps():
    # Запускаем AppleScript, который возвращает список всех открытых приложений
    script = 'tell application "System Events" to get name of every process whose background only is false'
    output = subprocess.check_output(['osascript', '-e', script])
    # Преобразуем вывод в список строк
    output = output.decode('utf-8').strip().split(', ')
    # Возвращаем список приложений
    return output


def get_active_app_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    """
    output = subprocess.check_output(["osascript", "-e", script])
    return output.strip().decode("utf-8")


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
        self.resize(840, 580)
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

        self.blocked_apps = {'Notion': 0}
        self.blocked_apps_for_percents = {'Notion': 1}  # На ноль секунд нельзя заблокировать

        self.stats_apps = {}
        # -----

        self.timer = QTimer()  # таймер
        self.timer.timeout.connect(self.update_data)  # подключаем сигнал таймера к слоту update_data
        self.timer.start(1000)  # таймер с интервалом в 1000 миллисекунд
        self.active_app = None

        self.time_left_block_app = 0  # Сколько времени осталось у заблокированного приложения
        self.time_spent = 0  # Времени проведено в приложении

        self.total_time = 3  # секунд - хранение общего времени
        self.total_time_for_percents = 3  # Переменная для создания бара
        self.password = "1234"  # # для хранения пароля

        self.button_exit.clicked.connect(self.close)

        self.flag = True

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

        if ok and password == self.password:
            event.accept()
        else:
            QMessageBox.warning(self, "Неверный пароль", "Вы ввели неверный пароль. Попробуйте еще раз.")
            event.ignore()

    def update_data(self):
        current_app = get_active_app_name()
        if self.total_time > 0 and self.flag:
            if current_app != "Finder":
                self.total_time -= 1
                if current_app != self.active_app:
                    if self.time_spent > 5:
                        if self.active_app in self.stats_apps:
                            self.stats_apps[self.active_app] += self.time_spent
                        else:
                            self.stats_apps[self.active_app] = self.time_spent
                    self.time_spent = 0
                    if self.active_app in self.blocked_apps:
                        self.blocked_apps[self.active_app] = self.time_left_block_app
                    self.active_app = current_app
                    if current_app in self.blocked_apps:
                        if self.blocked_apps[current_app] <= 1:
                            close_app(current_app)
                            self.time_left_block_app = 0
                            QMessageBox.warning(self, f"Время {current_app} вышло",
                                                "Вы больше не сможете открыть приложение сегодня")
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
                            QMessageBox.warning(self, f"Время {current_app} вышло",
                                                "Вы больше не можете находиться в приложении")
                        else:
                            self.time_left_block_app -= 1
                    else:
                        self.time_left_block_app = self.total_time

                self.time_all_time.setText(time.strftime("%H:%M:%S", time.gmtime(self.total_time)))
                self.time_active_app.setText(time.strftime("%H:%M:%S", time.gmtime(self.time_left_block_app)))

                if self.active_app in self.blocked_apps:
                    if self.time_left_block_app > 1:
                        self.progress_bar_active_app.setProperty("value", 100 * self.blocked_apps[self.active_app] /
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
