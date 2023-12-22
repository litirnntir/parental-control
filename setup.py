"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py
    python setup.py py2app -A
"""

from setuptools import setup

APP_NAME = 'Croak - Child Lock'
APP = ['main.py']
DATA_FILES = ['background.png', 'background_settings.png', 'settings.json', 'check_icon.png', 'correct_password.png',
              'incorrect_password.png', 'blocked_apps.json', 'blocked_apps_for_percents.json', 'stats_apps.json', 'code.json']
OPTIONS = {
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': 'Desktop parents control',
        'CFBundleVersion': '0.1.0 stable',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': 'Copyright (c) 2023 Gorbuntsova A.A., All rights reserves'
    },
    'iconfile': 'croak-logo.icns',
    'packages': ['PyQt6', 'osascript', 'PyQt6-Charts', 'PyQt6-Charts-Qt6', 'requests', 'openpyxl', 'telebot', 'multiprocessing']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
