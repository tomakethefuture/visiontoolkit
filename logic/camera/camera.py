"""
python 3.7.9

Module to call the camera
"""
import cv2 as cv
from PIL import Image
import numpy as np

class Camera:
    """Camera module
    """

    def open(self, cam:int) -> None:
        """Open the camera
        """
        while True:
            ret, frame = cv.VideoCapture(0).read()
            im = Image.fromarray(np.uint8(frame)*255)
            im.show()


camera = Camera()
camera.open(0)