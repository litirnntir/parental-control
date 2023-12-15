import subprocess
import time


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
