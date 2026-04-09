import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource. 
    Works for development and for PyInstaller's --onefile mode.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Standard mode
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
