from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox


def incorrect_password():
    msg = QMessageBox()
    pixmap = QPixmap("incorrect_password.png")
    msg.setIconPixmap(pixmap)
    msg.setText("Неверный пароль! Попробуйте еще раз.")
    msg.setWindowTitle("Ошибка")
    msg.exec()


def correct_change_password():
    msg = QMessageBox()
    pixmap = QPixmap("correct_password.png")
    msg.setIconPixmap(pixmap)
    msg.setText("Пароль изменен.")
    msg.setWindowTitle("Успешно!")
    msg.exec()


def correct(text):
    msg = QMessageBox()
    pixmap = QPixmap("check_icon.png")
    msg.setIconPixmap(pixmap)
    msg.setText(text)
    msg.setWindowTitle("Успешно!")
    msg.exec()
