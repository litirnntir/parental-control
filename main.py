import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog
from PyQt6.QtCore import QTimer, Qt
import time
from PyQt6.QtGui import QPalette, QBrush, QPixmap

APP_NAME = 'Croak - Child Lock'


def close_app(app_name):
    subprocess.call(f"killall {app_name}", shell=True)


def get_active_app_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    """
    output = subprocess.check_output(["osascript", "-e", script])
    return output.strip().decode("utf-8")


class AppTracker(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # безрамочный интерфейс
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)  # прозрачное окно

        # Загрузите изображение из файла или ресурса
        background_image = "background.png"  # Укажите путь к вашему файлу
        pix = QPixmap(background_image)  # Создайте объект QPixmap из изображения

        # Создайте палитру и кисть для вашего виджета
        pal = QPalette()  # Создайте пустую палитру
        pal.setBrush(self.backgroundRole(), QBrush(pix))  # Установите кисть с изображением для роли фона
        self.setPalette(pal)  # Примените палитру к вашему виджету

        self.setWindowTitle(APP_NAME)
        self.resize(840, 580)
        self.app_label = QLabel("Активное приложение:")
        self.time_label = QLabel("Время в приложении:")
        self.total_label = QLabel("Общее время:")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.app_label)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.total_label)
        self.setLayout(self.layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.active_app = None
        self.time_spent = 0
        self.total_time = 0
        self.password = "1234"

    def update_data(self):
        current_app = get_active_app_name()
        if current_app != self.active_app:
            self.active_app = current_app
            self.time_spent = 0
            self.app_label.setText(f"Активное приложение: {self.active_app}")
        else:
            self.time_spent += 1
            time_str = time.strftime("%H:%M:%S", time.gmtime(self.time_spent))
            self.time_label.setText(f"Время в приложении {self.active_app}: {time_str}")
        self.total_time += 1
        total_str = time.strftime("%H:%M:%S", time.gmtime(self.total_time))
        self.total_label.setText(f"Общее время: {total_str}")

    def closeEvent(self, event):
        text, ok = QInputDialog.getText(self, "Подтверждение выхода", "Введите пароль:")
        if ok and text == self.password:
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
window = AppTracker()
window.show()
sys.exit(app.exec())
