"""
Python 3.7.9

Construct the ribbon buttons
"""

from dearpygui.core import add_button


class RibbonButton:
    """Draw opencv mapping feature as button
    """

    @staticmethod
    def generate():
        """pop the buttons
        """
        add_button('FREAK')