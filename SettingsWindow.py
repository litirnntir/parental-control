from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QLineEdit, QFormLayout, QFileDialog)
from PyQt6.QtCore import Qt, QTime

import settings
from settings import password, total_time
import json


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.initUI()
        self.password = password

    def initUI(self):
        # Создаем 5 кнопок
        self.button1 = QPushButton('Настройки')
        self.button2 = QPushButton('Лимиты')
        self.button3 = QPushButton('Статистика')
        self.button4 = QPushButton('Коды')
        self.button5 = QPushButton('Отправить')

        # Создаем stackedWidget с 5 страницами
        self.stackedWidget = QStackedWidget()
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.page4 = QWidget()
        self.page5 = QWidget()
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)
        self.stackedWidget.addWidget(self.page4)
        self.stackedWidget.addWidget(self.page5)

        self.label1 = QLabel('', self.page1)
        self.label2 = QLabel('Это текст для кнопки 2', self.page2)
        self.label3 = QLabel('Это текст для кнопки 3', self.page3)
        self.label4 = QLabel('Это текст для кнопки 4', self.page4)
        self.label5 = QLabel('Это текст для кнопки 5', self.page5)

        ###########
        self.time_label = QLabel("Установить лимит времени в минутах:", self.page1)
        self.time_spinbox = QSpinBox(self.page1)
        self.time_spinbox.setRange(0, 1440)  # Минуты в сутках
        # Изменяем суффикс на пустую строку
        self.time_spinbox.setSuffix(" минут")
        # Изменяем шаг на 15 минут
        self.time_spinbox.setSingleStep(15)
        self.time_spinbox.setValue(0)
        self.time_spinbox.valueChanged.connect(self.update_time)
        # Добавляем новый атрибут для хранения формата времени
        self.time_format = "hh:mm"
        self.select_button = QPushButton("Выбрать", self.page1)
        self.select_button.clicked.connect(self.select_time)
        self.total_time = 0  # Время в секундах

        self.password_label = QLabel("Сменить пароль", self.page1)
        self.old_password_edit = QLineEdit(self.page1)
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_edit = QLineEdit(self.page1)
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.change_password_button = QPushButton("Сменить пароль", self.page1)
        self.change_password_button.clicked.connect(self.change_password)

        self.directory_label = QLabel("Выбрать директорию для сохранения статистики", self.page1)
        self.directory_button = QPushButton("Выбрать", self.page1)
        self.directory_button.clicked.connect(self.select_directory)
        self.directory = ""  # Директория для сохранения

        # Создаем layout для первой страницы
        self.page1_layout = QVBoxLayout()
        self.page1_layout.addWidget(self.time_label)
        self.page1_layout.addWidget(self.time_spinbox)
        self.page1_layout.addWidget(self.select_button)
        self.page1_layout.addWidget(self.password_label)
        self.page1_layout.addStretch()
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Введите старый пароль", self.old_password_edit)
        self.form_layout.addRow("Введите новый пароль", self.new_password_edit)
        self.page1_layout.addLayout(self.form_layout)
        self.page1_layout.addWidget(self.change_password_button)
        self.page1_layout.addWidget(self.directory_label)
        self.page1_layout.addWidget(self.directory_button)
        self.page1.setLayout(self.page1_layout)

        # Связываем кнопки с функциями, которые переключают страницы
        self.button1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.button2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.button4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.button5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button1)
        self.hbox.addWidget(self.button2)
        self.hbox.addWidget(self.button3)
        self.hbox.addWidget(self.button4)
        self.hbox.addWidget(self.button5)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.stackedWidget)

        self.setLayout(self.vbox)

        self.setWindowTitle('Настройки')
        self.resize(840, 580)

        self.show()

    import json

    def update_time(self, value):
        # Вычисляем часы и минуты из значения
        hours = value // 60
        minutes = value % 60
        # Используем QTime для преобразования минут в формат времени
        time = QTime(hours, minutes)
        # Используем атрибут time_format для отображения времени в нужном формате
        self.time_label.setText(f"Установить лимит времени в минутах: {time.toString(self.time_format)}")

        # Открываем json файл с именем settings.json в режиме "r+"
        with open("settings.json", "r+") as f:
            # Загружаем словарь с данными из файла
            data = json.load(f)
            # Изменяем значение total_time в словаре
            data["total_time"] = value
            # Перемещаем курсор в начало файла
            f.seek(0)
            # Очищаем файл
            f.truncate()
            # Сохраняем словарь в json файл
            json.dump(data, f)

    def select_time(self):
        self.total_time = self.time_spinbox.value() * 60
        settings.total_time = self.time_spinbox.value() * 60
        print(f"Выбрано время: {self.total_time} секунд")

    def change_password(self):
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        # Открываем json файл с именем settings.json
        with open("settings.json", "r+") as f:
            # Пытаемся загрузить существующие данные из файла
            try:
                data = json.load(f)
            # Если файл пустой или невалидный, создаем новый словарь
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                data = {}

            # Проверяем, совпадает ли старый пароль с текущим
            if old_password == data["password"]:
                # Меняем пароль на новый
                self.password = new_password
                # Сохраняем новый пароль в словаре под ключом "password"
                data["password"] = self.password
                print(f"Пароль изменен на {self.password}")
            else:
                print("Неверный старый пароль")

            # Перемещаем курсор в начало файла
            f.seek(0)
            # Перезаписываем файл с новыми данными
            json.dump(data, f)
            # Обрезаем файл, чтобы удалить лишние данные
            f.truncate()

        # Закрываем файл
        f.close()

    def select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        print(f"Выбрана директория: {self.directory}")

    def closeEvent(self, event):
        self.main_window.update_settings()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    ex = SettingsWindow()
    app.exec()
