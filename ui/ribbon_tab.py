"""
# Python 3.7.9

generate header tab module
"""
from dearpygui.core import add_text
from dearpygui.simple import tab, tab_bar
from ui.ribbon_button_features import RibbonButton


class RibbonTab:

    """
    Module to generate the tab header
    """

    @staticmethod
    def generate():
        """generate the tab that provides the functionality
        """
        with tab_bar('Header_tab'):
            with tab('Mapping Features'):
                RibbonButton.generate()
            with tab('Image Processing'):
                add_text('process tab')
