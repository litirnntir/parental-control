from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QLineEdit, QFormLayout, QFileDialog, QMessageBox, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, QTime

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap, QBrush, QPalette
from PyQt6.QtWidgets import QMainWindow, QApplication

import settings
from QMessages import incorrect_password, correct_change_password, correct
from settings import password, total_time
import json
import time


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.initUI()
        self.password = password

    def initUI(self):

        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # безрамочный интерфейс
        background_image = "background_settings.png"
        pix = QPixmap(background_image)
        pal = QPalette()
        pal.setBrush(self.backgroundRole(), QBrush(pix))
        self.setPalette(pal)

        font_button = QtGui.QFont()
        font_button.setFamily("Oswald")
        font_button.setPointSize(24)

        font_h1 = QtGui.QFont()
        font_h1.setFamily("Oswald")
        font_h1.setPointSize(24)

        font_h2 = QtGui.QFont()
        font_h2.setFamily("Oswald")
        font_h2.setPointSize(18)

        # Создаем 5 кнопок
        self.button1 = QPushButton('Настройки')
        self.button1.setFont(font_button)
        self.button1.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button2 = QPushButton('Лимиты')
        self.button2.setFont(font_button)
        self.button2.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button3 = QPushButton('Статистика')
        self.button3.setFont(font_button)
        self.button3.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button4 = QPushButton('Коды')
        self.button4.setFont(font_button)
        self.button4.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.button5 = QPushButton('Отправить')
        self.button5.setFont(font_button)
        self.button5.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")

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

        self.label2 = QLabel('Это текст для кнопки 2', self.page2)
        self.label3 = QLabel('Это текст для кнопки 3', self.page3)
        self.label4 = QLabel('Это текст для кнопки 4', self.page4)
        self.label5 = QLabel('Это текст для кнопки 5', self.page5)

        ############# PAGE 1 #########################

        self.label1 = QLabel('', self.page1)
        self.time_label = QLabel("Установить лимит времени в минутах:", self.page1)
        self.time_label.setFont(font_h1)
        self.time_label.setStyleSheet("color: rgb(255, 255, 255);")
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
        self.select_button.setFont(font_button)
        self.select_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.select_button.clicked.connect(self.select_time)
        self.total_time = 0  # Время в секундах

        # Password

        self.password_label = QLabel("Сменить пароль", self.page1)
        self.password_label.setFont(font_h1)
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.old_password_edit = QLineEdit(self.page1)
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_edit = QLineEdit(self.page1)
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.change_password_button = QPushButton("Сменить пароль", self.page1)
        self.change_password_button.setFont(font_button)
        self.change_password_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.change_password_button.clicked.connect(self.change_password)

        # Directory

        self.directory_label = QLabel("Директория для сохранения статистики: Нет", self.page1)
        self.directory_label.setWordWrap(True)

        self.directory_label.setFont(font_h1)
        self.directory_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.directory_button = QPushButton("Выбрать директорию", self.page1)
        self.directory_button.setFont(font_button)
        self.directory_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
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
        # Добавляем отступы и выравнивание для формы ввода пароля
        self.form_layout.setContentsMargins(0, 0, 20, 20)
        self.form_layout.addRow("Введите старый пароль", self.old_password_edit)
        self.form_layout.addRow("Введите новый пароль", self.new_password_edit)
        # Установить белый цвет, размер 18 и шрифт Oswald для меток
        self.form_layout.labelForField(self.old_password_edit).setStyleSheet(
            "color: white; font-size: 18px; font-family: Oswald;")
        self.form_layout.labelForField(self.new_password_edit).setStyleSheet(
            "color: white; font-size: 18px; font-family: Oswald;")

        self.page1_layout.addLayout(self.form_layout)
        self.page1_layout.addWidget(self.change_password_button)
        self.page1_layout.addWidget(self.directory_label)
        self.page1_layout.addWidget(self.directory_button)
        self.page1.setLayout(self.page1_layout)

        ################# PAGE 2 ###################



        ################# PAGE 3 ###################

        ################# PAGE 4 ###################

        ################# PAGE 5 ###################

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
        self.setFixedSize(840, 580)

        self.show()

    import json

    def update_time(self, value):
        # Вычисляем часы и минуты из значения
        hours = value // 60
        minutes = value % 60
        # Используем QTime для преобразования минут в формат времени
        timee = QTime(hours, minutes)
        # Используем атрибут time_format для отображения времени в нужном формате
        self.time_label.setText(f"Установить лимит времени в минутах: {timee.toString(self.time_format)}")

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
        f.close()

    def select_time(self):
        self.total_time = self.time_spinbox.value() * 60
        settings.total_time = self.time_spinbox.value() * 60
        self.main_window.update_settings()
        t = time.gmtime(self.total_time)
        correct(f'Лимит общего времени изменился на {time.strftime("%H:%M", t)}')

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
                correct_change_password()
            else:
                incorrect_password()

            # Перемещаем курсор в начало файла
            f.seek(0)
            # Перезаписываем файл с новыми данными
            json.dump(data, f)
            # Обрезаем файл, чтобы удалить лишние данные
            f.truncate()
        self.main_window.update_settings()
        # Закрываем файл
        f.close()

    def select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        self.directory_label.setText(f"Директория для сохранения статистики: {self.directory}")
        with open("settings.json", "r") as f:
            data = json.load(f)
        data["directory"] = self.directory
        with open("settings.json", "w") as f:
            json.dump(data, f)
        self.main_window.update_settings()

    def closeEvent(self, event):
        self.main_window.update_settings()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    ex = SettingsWindow()
    app.exec()
