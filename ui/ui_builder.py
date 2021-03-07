"""
python 3.7.9

This is home page of the vision toolkit 5
"""
from dearpygui.core import *
from dearpygui.simple import *
from pyautogui import size
from ui.windows import Windows
from ui.menu import Menu

class UiBuilder:

    """UI building module
    """

    def __init__(self, width:int, height:int, theme='Dark') -> None:
        """UI main window configuration

        Args:
            width (int): width of the main window
            height (int): height of the main window
            theme (str, optional): window theme. Defaults to 'Dark'.
        """
        self.theme = theme
        self.width = width
        self.height = height

    def make_gui(self, app_name:str, font_size:int, width:int, height:int, ) -> None:
        """build main window

        Args:
            app_name (str): window name
            font_size (int): window font size
            width (int): window width
            height (int): window height
        """
        set_main_window_title(app_name)
        set_global_font_scale(font_size)
        set_main_window_size(width=width, height=height)
        set_main_window_pos(0, 0)
    
        with window('Main window', height=height, width=width, x_pos=0, y_pos=0, no_title_bar=True, autosize=False, no_move=True, no_collapse=True):
            Menu.generate()
        
        

    def run_gui(self) -> None:
        """initiate main ui
        """
        start_dearpygui(primary_window='Main Window')




        
