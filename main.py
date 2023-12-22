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

# Определяем список команд, которые будут отображаться в меню
commands = [
    telebot.types.BotCommand(command="/reset", description="Сбросить статистику"),
    telebot.types.BotCommand(command="/id", description="Получить id"),
    telebot.types.BotCommand(command="/stats", description="Получить статистику")
]

# Устанавливаем список команд для бота
bot.set_my_commands(commands)


@bot.message_handler(commands=["start"])
def start(message):
    # Открываем файл для чтения в бинарном режиме
    file = open("croak-logo.png", "rb")

    # Отправляем фото ботом с подписью и клавиатурой
    bot.send_photo(message.chat.id, file, caption=f"Добро пожаловать в Croak! Для настройки зайдите через приложение на компьютере")


@bot.message_handler(commands=["id"])
def id(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}. Используйте его для привязки приложения")


@bot.message_handler(commands=["stats"])
def stats(message):
    if int(message.chat.id) == int(chat_id):
        save_stats_to_file()
        # Открываем файл excel в режиме чтения
        file = open("data.xlsx", "rb")
        # Отправляем файл по chat_id
        bot.send_document(chat_id, file)
        # Закрываем файл
        file.close()
    else:
        bot.send_message(message.chat.id, f"У вас нет доступа к статистике!")


@bot.message_handler(commands=["reset"])
def reset(message):
    if int(message.chat.id) == int(chat_id):
        with open("stats_apps.json", "w") as f:
            json.dump({}, f)
        bot.send_message(message.chat.id, f"Статистика сброшена")
    else:
        bot.send_message(message.chat.id, f"У вас нет доступа к статистике!")


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
