import os
import sys

# Add the Youtube-MP3-Playlist directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.app_controller import AppController

def set_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)

if __name__ == "__main__":
    application_path = set_path()
    app_controller = AppController(application_path)
    app_controller.main_menu()