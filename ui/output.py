"""
python 3.7.9

Construct computation output
"""

from dearpygui.core import add_text
from dearpygui.simple import child

class Output:

    """
    The module create child window for the output
    """

    @staticmethod
    def generate():
        with child('Output child', width=200):
            add_text('Output')
