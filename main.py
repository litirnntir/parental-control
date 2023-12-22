import json
import multiprocessing
import sys

import telebot
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow

from system_functions import get_from_json, save_stats_to_file

TOKEN = get_from_json("settings.json")["TOKEN"]
chat_id = get_from_json("settings.json")["chat_id"]
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["id"])
def start(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}")


@bot.message_handler(commands=["stats"])
def stats(message):
    save_stats_to_file()
    # Открываем файл excel в режиме чтения
    file = open("data.xlsx", "rb")
    # Отправляем файл по chat_id
    bot.send_document(chat_id, file)
    # Закрываем файл
    file.close()


@bot.message_handler(commands=["reset"])
def reset(message):
    with open("stats_apps.json", "w") as f:
        json.dump({}, f)
    bot.send_message(message.chat.id, f"Статистика сброшена")


def run_bot():
    bot.polling()


def run_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    multiprocessing.freeze_support()
    time_process = multiprocessing.Process(target=run_window)
    bot_process = multiprocessing.Process(target=run_bot)

    bot_process.start()
    time_process.start()

    bot_process.join()
    time_process.join()
