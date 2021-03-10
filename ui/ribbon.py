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
    def generate(height:int) -> None:
        with child('tab'):
            set_item_height('tab', int(0.10*height))
            RibbonTab.generate()