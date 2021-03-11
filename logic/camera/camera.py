"""Camera construction
"""

import numpy as np
import cv2 as cv 
import queue 
from threading import Thread 
import datetime
import time

class Camera:
    """Camera manipulation module
    """

    def __init__(self) -> None:
        """Construct the controller
        """
        self.stop_thread = False
        self.stop_cam = False

    def start_thread(self, cam: cv.VideoCapture, queue:queue.Queue) -> None:
        """Thread to initiate webcam and queing the frame

        Args:
            cam (cv.VideoCapture): webcam id
            queue (queue.Queue): frame queue
        """
        while True:
            _, frame = cam.read()
            queue.put(frame)

            if self.stop_thread:
                break

    def open(self, device:int) -> None:
        """Initiate web cam

        Args:
            device (int): webcam id
        """
        try:
            frames = 0
            cur_fps = 0

            # initiate web cam and put the frame into thread queue
            cam = cv.VideoCapture(device, cv.CAP_DSHOW)
            frame_queue = queue.Queue(maxsize=0)

            # initiate the thread and pass queue frame to thread
            thread = Thread()
            t = Thread(target=self.start_thread, 
                args=(cam, frame_queue,),
                daemon=True)
            t.start()

            while True:
                if frame_queue.empty():
                    continue 
                
                last_time = datetime.datetime.now()
                frames += 1
                delta_time = datetime.datetime.now() - last_time
                elapse_time = delta_time.total_seconds()

                if (elapse_time != 0):
                    current_fps = np.around(frames / elapse_time, 1)

                img = frame_queue.get()
                if img is not None:
                    cv.imshow('output', img)
                
                cv.waitKey(1)
                if self.stop_cam:
                    self.stop_thread = True
                    break
                # if (key == 27):
                #     self.stop_thread = True
                #     break
        except:
            pass
        finally:
            cv.destroyAllWindows()
            cam.release()

    def close(self):
        self.stop_cam = True

cam = Camera()
