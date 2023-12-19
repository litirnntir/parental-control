import subprocess
import os
import signal


def apps_list():
    apps = []
    app_path = "/Applications"
    for file in os.listdir(app_path):
        if file.endswith(".app"):
            apps.append(file[:-4])
    return apps


def close_app(app_name):
    try:
        processes = os.popen("ps ax").readlines()
        for process in processes:
            if app_name in process:
                fields = process.split()
                pid = fields[0]
                os.kill(int(pid), signal.SIGTERM)
                print(f"Закрыли приложение {app_name}")
    except:
        pass


def get_open_apps():
    script = 'tell application "System Events" to get name of every process whose background only is false'
    output = subprocess.check_output(['osascript', '-e', script])
    output = output.decode('utf-8').strip().split(', ')
    return output


def get_active_app_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    """
    output = subprocess.check_output(["osascript", "-e", script])
    return output.strip().decode("utf-8")
