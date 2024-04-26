import sys
import os

import config


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if config.USE_PYINSTALLER_FUNCION_PATH:
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        if relative_path[0] == "\\":
            result = base_path + relative_path
        else:
            result = base_path + "\\" + relative_path
        return result
    else:
        return os.getcwd() + "\\" + relative_path
