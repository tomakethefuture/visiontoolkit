"""
python 3.7.9

Module to build the window
"""
from dearpygui.core import *
from dearpygui.simple import *
from ui.ribbon_tab import RibbonTab

class Ribbon:
    """
    Window building module
    """

    @staticmethod
    def generate():
        with child('tab', height=150):
            RibbonTab.generate()