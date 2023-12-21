from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox


def pop_up_message(text, icon_path=None, title="Успешно"):
    msg = QMessageBox()
    if icon_path:
        pixmap = QPixmap(icon_path)
        msg.setIconPixmap(pixmap)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.exec()
