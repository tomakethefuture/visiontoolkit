"""
python 3.7.9

Module to build the window
"""
from dearpygui.core import *
from dearpygui.simple import *

class Windows:
    """
    Window building module
    """

    @staticmethod
    def generate_window(window_name:str):
        add_about_window('sample')