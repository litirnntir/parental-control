import json
import multiprocessing
import os
import sys

import telebot
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow

from system_functions import get_from_json, save_stats_to_file, apps_list

TOKEN = get_from_json("settings.json")["TOKEN"]
chat_id = get_from_json("settings.json")["chat_id"]
bot = telebot.TeleBot(TOKEN)

# Определяем список команд, которые будут отображаться в меню
commands = [
    telebot.types.BotCommand(command="/add_code", description="Создать код"),
    telebot.types.BotCommand(command="/reset", description="Сбросить статистику"),
    telebot.types.BotCommand(command="/id", description="Получить id"),
    telebot.types.BotCommand(command="/stats", description="Получить статистику")
]

# Устанавливаем список команд для бота
bot.set_my_commands(commands)


# Определяем функцию, которая проверяет, существует ли приложение в списке
def app_exists(app):
    # Получаем список приложений
    apps = apps_list()
    # Проверяем, есть ли приложение в списке
    return app in apps


# Определяем функцию, которая добавляет код, приложение и время в файл code.json
def add_code(code, app, time):
    # Проверяем, существует ли файл code.json
    if os.path.exists("code.json"):
        # Открываем файл для чтения
        with open("code.json", "r") as f:
            # Загружаем данные из файла в словарь
            data = json.load(f)
    else:
        # Создаем пустой словарь
        data = {}
    # Добавляем код, приложение и время в словарь
    data[code] = {"app": app, "time": time}
    # Открываем файл для записи
    with open("code.json", "w") as f:
        # Сохраняем данные в файл в формате json
        json.dump(data, f, indent=4)


# Определяем функцию, которая обрабатывает команду добавить код
@bot.message_handler(commands=["add_code"])
def add_code_handler(message):
    # Отправляем сообщение с инструкцией
    bot.send_message(message.chat.id, "Введите код в формате: код, приложение, время в секундах")
    # Переходим в режим ожидания ответа пользователя
    bot.register_next_step_handler(message, get_code)


# Определяем функцию, которая получает код от пользователя
def get_code(message):
    # Получаем текст сообщения
    text = message.text
    # Проверяем, что текст содержит три элемента, разделенных запятыми
    if len(text.split(",")) == 3:
        # Разбиваем текст на код, приложение и время
        code, app, time = text.split(",")
        # Удаляем лишние пробелы
        code = code.strip()
        app = app.strip()
        time = time.strip()
        # Проверяем, что приложение существует
        if app_exists(app):
            # Добавляем код, приложение и время в файл code.json
            add_code(code, app, time)
            # Отправляем сообщение с подтверждением
            bot.send_message(message.chat.id, "Код успешно добавлен")
        else:
            # Отправляем сообщение с ошибкой
            bot.send_message(message.chat.id, "Ошибка: такого приложения нет в списке")
    else:
        # Отправляем сообщение с ошибкой
        bot.send_message(message.chat.id, "Ошибка: неверный формат ввода")


@bot.message_handler(commands=["start"])
def start(message):
    # Открываем файл для чтения в бинарном режиме
    file = open("croak-logo.png", "rb")

    # Отправляем фото ботом с подписью и клавиатурой
    bot.send_photo(message.chat.id, file,
                   caption=f"Добро пожаловать в Croak! Для настройки зайдите через приложение на компьютере")


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
