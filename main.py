# Импортируем необходимые модули
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer


# Создаем класс для нашего окна
class AppTracker(QWidget):
    def __init__(self):
        super().__init__()
        # Устанавливаем заголовок и размер окна
        self.setWindowTitle("App Tracker")
        self.resize(300, 100)
        # Создаем метки для отображения активного приложения и времени
        self.app_label = QLabel("Active app: None")
        self.time_label = QLabel("Time spent: 0 seconds")
        # Создаем вертикальный слой для размещения меток
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.app_label)
        self.layout.addWidget(self.time_label)
        self.setLayout(self.layout)
        # Создаем таймер для обновления данных каждую секунду
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        # Инициализируем переменные для хранения активного приложения и времени
        self.active_app = None
        self.time_spent = 0

    # Определяем функцию для получения активного приложения
    def get_active_app_name(self):
        script = """
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
        end tell
        return frontApp
        """
        output = subprocess.check_output(["osascript", "-e", script])
        return output.strip().decode("utf-8")

    # Определяем функцию для обновления данных
    def update_data(self):
        # Получаем активное приложение
        current_app = self.get_active_app_name()
        # Если оно изменилось, то сбрасываем время и обновляем метку
        if current_app != self.active_app:
            self.active_app = current_app
            self.time_spent = 0
            self.app_label.setText(f"Active app: {self.active_app}")
        # Иначе увеличиваем время на одну секунду и обновляем метку
        else:
            self.time_spent += 1
            self.time_label.setText(f"Time spent: {self.time_spent} seconds")


# Создаем приложение и запускаем его
app = QApplication(sys.argv)
window = AppTracker()
window.show()
sys.exit(app.exec())
