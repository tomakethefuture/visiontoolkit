"""
python 3.7.9

Construct computation output
"""

from dearpygui.core import *
from dearpygui.simple import *

class Output:

    """
    The module create child window for the output
    """

    @staticmethod
    def generate(width):
        with child('Output child', no_scrollbar=True):
            set_item_width('Output child', int(0.10*width))
            add_text('Output')
