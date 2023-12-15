import subprocess
import os


def close_app(app):
    subprocess.call(f"killall {app}", shell=True)


# Список всех открытых приложений
def apps_list():
    output = subprocess.check_output(
        ["osascript", "-e",
         "tell application \"System Events\" to get name of (processes where background only is false)"])

    # Преобразуем вывод в список строк, разделенных запятыми
    output = output.decode("utf-8").split(", ")

    print("Список открытых приложений:")
    for app in output:
        print(app)


def get_active_app_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    """
    output = subprocess.check_output(["osascript", "-e", script])
    return output.strip().decode("utf-8")


def list_all_applications():
    # Создаем пустой список для хранения имен приложений
    apps = []
    # Получаем путь к папке Applications
    app_path = "/Applications"
    # Перебираем все файлы в папке Applications
    for file in os.listdir(app_path):
        # Проверяем, является ли файл приложением (имеет расширение .app)
        if file.endswith(".app"):
            # Добавляем имя приложения в список
            apps.append(file)
    # Выводим список приложений на экран
    for app in apps:
        print(app)
