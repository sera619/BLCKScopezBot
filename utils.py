import sys
import os
from pathlib import Path

def resource_path(relative: str) -> Path:
    """
    Get absolute path to resource, works in dev and PyInstaller exe.
    """
    try:
        # PyInstaller temp folder
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # normal script
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent  # exe mode
        else:
            base_path = Path(__file__).parent       # dev mode
    return base_path / relative
