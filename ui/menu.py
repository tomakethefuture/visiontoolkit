"""
python 3.7.9

Menu generation module
"""

from dearpygui.core import *
from dearpygui.simple import menu, menu_bar


class Menu():
    """
    Module to handle UI menus
    """

    @staticmethod
    def generate() -> None:
        """
        generate menu and menu items
        """
        with menu_bar('Main Menu'):
            with menu('File'):
                add_menu_item('Save')
                add_menu_item('Close')
            with menu('Editor'):
                pass
            with menu('Preferences'):
                pass
