import json
import time

from PyQt6 import QtGui
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtGui import QPixmap, QBrush, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import (QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QLineEdit, QFormLayout, QFileDialog, QTableWidget, QHeaderView,
                             QAbstractItemView, QTimeEdit, QComboBox, QTableWidgetItem,
                             QLCDNumber, QColorDialog)

import settings
from QMessages import pop_up_message
from system_functions import apps_list, get_from_json


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.initUI()
        self.password = get_from_json("settings.json")["password"]

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

        font_small_button = QtGui.QFont()
        font_small_button.setFamily("Oswald")
        font_small_button.setPointSize(18)

        font_h1 = QtGui.QFont()
        font_h1.setFamily("Oswald")
        font_h1.setPointSize(24)

        font_h2 = QtGui.QFont()
        font_h2.setFamily("Oswald")
        font_h2.setPointSize(18)

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

        ############# PAGE 1 #########################

        self.label1 = QLabel('', self.page1)
        self.time_label = QLabel("Установить лимит времени:", self.page1)
        self.time_label.setFont(font_h1)
        self.time_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.time_spinbox = QSpinBox(self.page1)
        self.time_spinbox.setRange(0, 1440)  # Минуты в сутках
        self.time_spinbox.setSuffix(" минут")
        self.time_spinbox.setSingleStep(15)
        self.time_spinbox.setValue(0)
        self.time_spinbox.valueChanged.connect(self.p1_update_time)
        self.time_format = "hh:mm"
        self.select_button = QPushButton("Выбрать", self.page1)
        self.select_button.setFont(font_button)
        self.select_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.select_button.clicked.connect(self.p1_select_time)
        self.total_time = 0

        self.password_label = QLabel("Сменить пароль", self.page1)
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.change_password_button.clicked.connect(self.p1_change_password)

        self.directory_label = QLabel("Директория для сохранения статистики: Нет", self.page1)
        self.directory_label.setWordWrap(True)

        self.directory_label.setFont(font_h1)
        self.directory_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.directory_button = QPushButton("Выбрать директорию", self.page1)
        self.directory_button.setFont(font_button)
        self.directory_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.directory_button.clicked.connect(self.p1_select_directory)
        self.directory = ""

        self.page1_layout = QVBoxLayout()
        self.page1_layout.addWidget(self.time_label)
        self.page1_layout.addWidget(self.time_spinbox)
        self.page1_layout.addWidget(self.select_button)
        self.page1_layout.addWidget(self.password_label)
        self.page1_layout.addStretch()
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 20, 20)
        self.form_layout.addRow("Введите старый пароль", self.old_password_edit)
        self.form_layout.addRow("Введите новый пароль", self.new_password_edit)
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

        self.page2_layout = QVBoxLayout()

        self.label = QLabel("Добавить лимит на приложение")
        self.label.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page2_layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(apps_list())
        self.page2_layout.addWidget(self.combo)

        self.time = QTimeEdit()
        self.time.setDisplayFormat("hh:mm")
        self.time.setTime(QTime(0, 0))
        self.page2_layout.addWidget(self.time)

        self.set_limit = QPushButton("Установить лимит")
        self.set_limit.setFont(font_button)
        self.set_limit.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.set_limit.clicked.connect(self.p2_set_limit_clicked)
        self.page2_layout.addWidget(self.set_limit)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Приложение", "Время"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.p2_update_table()
        self.page2_layout.addWidget(self.table)

        self.delete = QPushButton("Удалить лимит")
        self.delete.setFont(font_button)
        self.delete.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.delete.clicked.connect(self.p2_delete_clicked)
        self.page2_layout.addWidget(self.delete)

        self.page2.setLayout(self.page2_layout)

        ################# PAGE 3 ###################

        self.page3_layout = QVBoxLayout()
        self.page3.setLayout(self.page3_layout)

        self.timer = QLCDNumber()
        self.timer.setDigitCount(8)
        self.timer.display("00:00:00")

        self.timer_label = QLabel("Статистика за последние: ")
        self.timer_label.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")

        self.timer_layout = QHBoxLayout()
        self.timer_layout.addWidget(self.timer_label)
        self.timer_layout.addWidget(self.timer)

        self.page3_layout.addLayout(self.timer_layout)

        self.chart = QChart()
        self.chart.setTitle("Диаграмма")
        self.chart.setTitleFont(font_h1)

        self.color_button = QPushButton("Выбрать цвет фона")
        self.color_button.setFont(font_button)
        self.color_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        # Подключите сигнал нажатия кнопки к слоту color_picker
        self.color_button.clicked.connect(self.p3_color_picker)
        # Добавьте кнопку в ваш макет
        self.page3_layout.addWidget(self.color_button)

        self.series = QPieSeries()
        self.colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 255, 0),
                       QColor(0, 255, 255)]

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.page3_layout.addWidget(self.chart_view)

        self.reset_button = QPushButton("Сбросить статистику")
        self.reset_button.setFont(font_button)
        self.reset_button.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.reset_button.clicked.connect(self.p2_reset_stats)

        self.page3_layout.addWidget(self.reset_button)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.p3_update_data)
        self.update_timer.start(1000)

        ################# PAGE 4 ###################

        # Создаем layout для четвертой страницы
        self.page4_layout = QVBoxLayout()

        # Создаем заголовок
        self.page4_title = QLabel("Коды для дополнительного времени")
        self.page4_title.setStyleSheet("color: white; font-size: 24px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_title)

        # Создаем подзаголовок
        self.page4_subtitle = QLabel("Код для приложения:")
        self.page4_subtitle.setStyleSheet("color: white; font-size: 18px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_subtitle)

        # Создаем форму для ввода кода
        self.page4_code = QLineEdit()
        self.page4_code.setPlaceholderText("Введите код")
        self.page4_layout.addWidget(self.page4_code)

        # Создаем выпадающий список со всеми приложениями
        self.page4_apps = QComboBox()
        self.page4_apps.addItems(apps_list())  # Используем существующую функцию apps_list
        self.page4_layout.addWidget(self.page4_apps)

        # Создаем выбор времени со стрелками
        self.page4_time = QTimeEdit()
        self.page4_time.setDisplayFormat("hh:mm")
        self.page4_time.setTime(QTime(0, 0))  # Устанавливаем начальное время 00:00
        self.page4_layout.addWidget(self.page4_time)

        # Создаем кнопку "Добавить код"
        self.page4_add = QPushButton("Добавить код")
        self.page4_add.setFont(font_small_button)
        self.page4_add.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.page4_add.clicked.connect(self.p4_add_code)  # Связываем кнопку с функцией add_code
        self.page4_layout.addWidget(self.page4_add)

        # Создаем заголовок для кода для общего времени
        self.page4_total_title = QLabel("Код для общего времени")
        self.page4_total_title.setStyleSheet("color: white; font-size: 18px; font-family: Oswald;")
        self.page4_layout.addWidget(self.page4_total_title)

        # Создаем форму для ввода кода для общего времени
        self.page4_total_code = QLineEdit()
        self.page4_total_code.setPlaceholderText("Введите код")
        self.page4_layout.addWidget(self.page4_total_code)

        # Создаем выбор времени со стрелками для общего времени
        self.page4_total_time = QTimeEdit()
        self.page4_total_time.setDisplayFormat("hh:mm")
        self.page4_total_time.setTime(QTime(0, 0))  # Устанавливаем начальное время 00:00
        self.page4_layout.addWidget(self.page4_total_time)

        # Создаем кнопку "Добавить код" для общего времени
        self.page4_total_add = QPushButton("Добавить код")
        self.page4_total_add.setFont(font_small_button)
        self.page4_total_add.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.page4_total_add.clicked.connect(self.p4_add_total_code)  # Связываем кнопку с функцией add_total_code
        self.page4_layout.addWidget(self.page4_total_add)

        # Создаем таблицу с данными из code.json
        self.page4_table = QTableWidget()
        self.page4_table.setColumnCount(3)  # Устанавливаем три столбца
        self.page4_table.setHorizontalHeaderLabels(["Код", "Приложение", "Время"])  # Устанавливаем заголовки столбцов
        self.page4_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # Растягиваем столбцы по ширине
        self.page4_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)  # Устанавливаем выделение по строкам
        self.page4_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)  # Устанавливаем одиночное выделение
        self.page4_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Отключаем редактирование ячеек
        self.page4_table.verticalHeader().hide()  # Скрываем вертикальные заголовки
        self.page4_table.setRowCount(0)  # Устанавливаем нулевое количество строк
        self.page4_layout.addWidget(self.page4_table)

        # Создаем кнопку "Удалить"
        self.page4_delete = QPushButton("Удалить код")
        self.page4_delete.setFont(font_button)
        self.page4_delete.setStyleSheet(
            "border-radius: 10px;color: rgb(255, 255, 255);background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.33, fx:0.5, fy:0.5, stop:0 rgba(26, 95, 146, 255), stop:1 rgba(255, 255, 255, 0));")
        self.page4_delete.clicked.connect(self.p4_delete_code)  # Связываем кнопку с функцией delete_code
        self.page4_layout.addWidget(self.page4_delete)

        # Устанавливаем layout для четвертой страницы
        self.page4.setLayout(self.page4_layout)

        # Загружаем данные из code.json в таблицу
        self.p4_load_data()

        ################# PAGE 5 ###################

        ########################################

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

    def p4_add_total_code(self):
        # Получаем введенный код и время для общего времени
        code = self.page4_total_code.text()
        time = self.page4_total_time.time().toString("hh:mm")

        hours, minutes = time.split(":")
        seconds = 0
        # Преобразуем часы и минуты в целые числа
        hours = int(hours)
        minutes = int(minutes)

        # Проверяем, что часы и минуты находятся в допустимом диапазоне
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            # Переводим часы и минуты в секунды, умножая на соответствующие коэффициенты
            seconds = hours * 3600 + minutes * 60

        # Проверяем, что код не пустой
        if code:
            # Открываем файл code.json для чтения и записи
            with open("code.json", "r+") as f:
                # Загружаем данные из файла в словарь
                data = json.load(f)
                # Добавляем или обновляем данные по коду для общего времени
                data[code] = {"Приложение": 'total', "Время": seconds}
                # Перемещаем указатель в начало файла
                f.seek(0)
                # Записываем обновленный словарь в файл
                json.dump(data, f, ensure_ascii=False, indent=4)
                # Обрезаем файл до текущего размера
                f.truncate()
            # Очищаем поле ввода кода для общего времени
            self.page4_total_code.clear()
            # Обновляем таблицу с данными
            self.p4_load_data()
        else:
            # Выводим сообщение об ошибке
            print("Код не может быть пустым")

    def p4_add_code(self):
        # Получаем введенный код, выбранное приложение и время
        code = self.page4_code.text()
        app = self.page4_apps.currentText()
        time = self.page4_time.time().toString("hh:mm")

        hours, minutes = time.split(":")
        seconds = 0
        # Преобразуем часы и минуты в целые числа
        hours = int(hours)
        minutes = int(minutes)

        # Проверяем, что часы и минуты находятся в допустимом диапазоне
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            # Переводим часы и минуты в секунды, умножая на соответствующие коэффициенты
            seconds = hours * 3600 + minutes * 60

        # Проверяем, что код не пустой
        if code:
            # Открываем файл code.json для чтения и записи
            with open("code.json", "r+") as f:
                # Загружаем данные из файла в словарь
                data = json.load(f)
                # Добавляем или обновляем данные по коду
                data[code] = {"Приложение": app, "Время": seconds}
                # Перемещаем указатель в начало файла
                f.seek(0)
                # Записываем обновленный словарь в файл
                json.dump(data, f, ensure_ascii=False, indent=4)
                # Обрезаем файл до текущего размера
                f.truncate()
            # Очищаем поле ввода кода
            self.page4_code.clear()
            # Обновляем таблицу с данными
            self.p4_load_data()
        else:
            # Выводим сообщение об ошибке
            print("Код не может быть пустым")

    def p4_delete_code(self):
        # Получаем индекс выделенной строки
        row = self.page4_table.currentRow()
        # Проверяем, что строка выделена
        if row != -1:
            # Получаем код из первой ячейки строки
            code = self.page4_table.item(row, 0).text()
            # Открываем файл code.json для чтения и записи
            with open("code.json", "r+") as f:
                # Загружаем данные из файла в словарь
                data = json.load(f)
                # Удаляем данные по коду
                data.pop(code, None)
                # Перемещаем указатель в начало файла
                f.seek(0)
                # Записываем обновленный словарь в файл
                json.dump(data, f, ensure_ascii=False, indent=4)
                # Обрезаем файл до текущего размера
                f.truncate()
            # Обновляем таблицу с данными
            self.p4_load_data()
        else:
            # Выводим сообщение об ошибке
            print("Нет выделенной строки")

    def p4_load_data(self):
        # Открываем файл code.json для чтения
        with open("code.json", "r") as f:
            # Загружаем данные из файла в словарь
            data = json.load(f)
            # Устанавливаем количество строк в таблице равное количеству кодов
            self.page4_table.setRowCount(len(data))
            # Проходим по всем кодам в словаре
            for i, code in enumerate(data):
                # Получаем приложение и время по коду
                app = data[code]["Приложение"]
                time = data[code]["Время"]
                # Создаем ячейки с кодом, приложением и временем
                code_item = QTableWidgetItem(code)
                app_item = QTableWidgetItem(app)
                time_item = QTableWidgetItem(time)
                # Добавляем ячейки в соответствующие столбцы и строки таблицы
                self.page4_table.setItem(i, 0, code_item)
                self.page4_table.setItem(i, 1, app_item)
                self.page4_table.setItem(i, 2, time_item)

    def p3_color_picker(self):
        # Откройте диалог выбора цвета и получите выбранный цвет
        color = QColorDialog.getColor()
        # Если цвет был выбран, установите его в качестве цвета фона для диаграммы
        if color.isValid():
            self.chart.setBackgroundBrush(QBrush(color))

    def p3_update_data(self):
        with open("stats_apps.json", "r") as f:
            stats = json.load(f)

        total_time = sum(stats.values())

        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.timer.display(time_str)

        self.series.clear()

        for i, (app, time) in enumerate(stats.items()):
            percentage = round(time / total_time * 100, 2)
            self.series.append(f"{app} ({percentage}%)", time)
            self.series.slices()[i].setBrush(self.colors[i % len(self.colors)])

        self.chart.addSeries(self.series)

    def p2_reset_stats(self):
        with open("stats_apps.json", "w") as f:
            json.dump({}, f)

        self.series.clear()
        self.timer.display("00:00:00")

    def p2_set_limit_clicked(self):
        import json
        app2 = self.combo.currentText()
        time2 = self.time.time().toString("hh:mm")
        h, m = time2.split(':')
        time2 = int(h) * 3600 + int(m) * 60
        with open("blocked_apps.json", "r") as file:
            data = json.load(file)
        data[app2] = time2
        with open("blocked_apps.json", "w") as file:
            json.dump(data, file)
        with open("blocked_apps_for_percents.json", "r") as file:
            data = json.load(file)
        data[app2] = time2
        with open("blocked_apps_for_percents.json", "w") as file:
            json.dump(data, file)
        self.p2_update_table()
        self.main_window.update_settings()
        pop_up_message(text=f"Лимит для {app2} установлен", icon_path="check_icon.png", title="Успешно")

    def p2_update_table(self):
        import json
        with open("blocked_apps.json", "r") as file:
            data = json.load(file)
        self.table.setRowCount(len(data))
        row = 0
        for app, time in data.items():
            app_item = QTableWidgetItem(app)
            h, m = divmod(time, 3600)
            m, s = divmod(m, 60)
            time_str = f'{h:02d}:{m:02d}'
            time_item = QTableWidgetItem(time_str)
            self.table.setItem(row, 0, app_item)
            self.table.setItem(row, 1, time_item)
            row += 1

    def p2_delete_clicked(self):
        import json
        row = self.table.currentRow()
        if row != -1:
            app = self.table.item(row, 0).text()
            with open("blocked_apps.json", "r") as file:
                data = json.load(file)
            del data[app]
            with open("blocked_apps.json", "w") as file:
                json.dump(data, file)
            with open("blocked_apps_for_percents.json", "r") as file:
                data = json.load(file)

            del data[app]
            with open("blocked_apps_for_percents.json", "w") as file:
                json.dump(data, file)
            self.p2_update_table()
        self.main_window.update_settings()

    def p1_update_time(self, value):
        hours = value // 60
        minutes = value % 60
        timee = QTime(hours, minutes)
        self.time_label.setText(f"Установить лимит времени: {timee.toString(self.time_format)}")

        with open("settings.json", "r+") as f:
            data = json.load(f)
            data["total_time"] = value
            f.seek(0)
            f.truncate()
            json.dump(data, f)
        f.close()
        self.main_window.update_settings()

    def p1_select_time(self):
        self.total_time = self.time_spinbox.value() * 60
        settings.total_time = self.time_spinbox.value() * 60
        self.main_window.update_settings()
        t = time.gmtime(self.total_time)
        pop_up_message(text=f'Лимит общего времени изменился на {time.strftime("%H:%M", t)}',
                       icon_path="check_icon.png",
                       title="Успешно")

    def p1_change_password(self):
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        with open("settings.json", "r+") as f:
            try:
                data = json.load(f)

            except (json.decoder.JSONDecodeError, FileNotFoundError):
                data = {}

            if old_password == data["password"]:
                self.password = new_password
                data["password"] = self.password
                pop_up_message(text="Пароль изменен.", icon_path="correct_password.png",
                               title="Успешно")
            else:
                pop_up_message(text="Неверный пароль! Попробуйте еще раз.", icon_path="incorrect_password.png",
                               title="Ошибка")

            f.seek(0)
            json.dump(data, f)
            f.truncate()
        self.main_window.update_settings()
        f.close()

    def p1_select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        self.directory_label.setText(f"Директория для сохранения статистики: {self.directory}")
        with open("settings.json", "r") as f:
            data = json.load(f)
        data["directory"] = self.directory
        with open("settings.json", "w") as f:
            json.dump(data, f)
        self.main_window.update_settings()

    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    ex = SettingsWindow()
    app.exec()
