"""
python 3.7.9

Main workspace
"""

from dearpygui.core import add_text
from dearpygui.simple import child

class Workspace:
    """
    Working space of the vision toolkit
    """

    @staticmethod
    def generate() -> None:
        """generate workspace
        """
        with child('Main Workspace', no_scrollbar=True):
            add_text('workspace')