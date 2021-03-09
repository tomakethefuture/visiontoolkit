"""
python 3.7.9

Main workspace
"""

from dearpygui.core import add_text, set_style_touch_extra_padding
from dearpygui.simple import child

class Workspace:
    """
    Working space of the vision toolkit
    """

    @staticmethod
    def generate():
        """generate workspace
        """
        set_style_touch_extra_padding(100, 100)
        with child('Main Workspace'):
            add_text('workspace')