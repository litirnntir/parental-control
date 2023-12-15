"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py
    python setup.py py2app -A
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'label.icns',
    'packages': ['psutil']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
