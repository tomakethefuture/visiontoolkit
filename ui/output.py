"""
python 3.7.9

Construct computation output
"""

from dearpygui.core import *
from dearpygui.simple import *
import os
import sys 

sys.path.append(os.path.join(sys.path[0], '../'))
from logic.camera.camera import Camera

class Output:

    """
    The module create child window for the output
    """
        
    @staticmethod
    def generate(width):
        with child('Output child', no_scrollbar=True):
            set_item_width('Output child', int(0.10*width))
            add_text('Output')
            Camera().open(0)
            