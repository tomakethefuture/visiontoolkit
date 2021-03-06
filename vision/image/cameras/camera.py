import os
import time
import logging
import traceback

import cv2

class camera:
    _log = None
    _camera = None
    _config = None
    _retrying = None
    
    def __init__(self):
        self._log = logging.getLogger("FMC.camera")
        self._retrying = 0 
        pass
        
    def create(self,dict_config):
        self._config = dict_config
        self._log.info("{}".format(dict_config.source_name))
        
        self.close()   
        #temporary camera source
        camera =None
        
        started = False
        while not started:
            try:
                
                #Create camera object
                if os.name == 'nt' and dict_config.camera_directshow:
                    self._log.info("Use DirectShow")
                    camera = cv2.VideoCapture() ### Logitect WebCam window 16:9 directshow output
                    camera.open(int(dict_config.camera),cv2.CAP_DSHOW)
                elif os.name != 'nt' and dict_config.camera_V4L2_format is not None:
                    #https://answers.opencv.org/question/41899/changing-pixel-format-yuyv-to-mjpg-when-capturing-from-webcam/
                    self._log.info("Use V4L2")
                    camera = cv2.VideoCapture(int(dict_config.camera),cv2.CAP_V4L2) ### For Linux compatible
                    f=list(dict_config.camera_V4L2_format)
                    camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(f[0],f[1],f[2],f[3]))
                else:
                    self._log.info("Normal")
                    camera = cv2.VideoCapture(int(dict_config.camera))
                    
                if dict_config.camera_resolution_width is not None:
                    camera.set(cv2.CAP_PROP_FRAME_WIDTH,dict_config.camera_resolution_width)
                if dict_config.camera_resolution_height is not None:
                    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,dict_config.camera_resolution_height)    
                if dict_config.camera_focus is not None:
                    camera.set(cv2.CAP_PROP_AUTOFOCUS,0)
                    camera.set(cv2.CAP_PROP_FOCUS,dict_config.camera_focus)
                if dict_config.camera_exposure is not None:
                    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
                    camera.set(cv2.CAP_PROP_EXPOSURE,dict_config.camera_exposure)
                if dict_config.camera_framerate is not None:
                    camera.set(cv2.CAP_PROP_FPS,dict_config.camera_exposure)
                #camera.set(cv2.CAP_PROP_FPS, 15)
                success, image = camera.read()
                if not success:
                    self._log.error("Camera '"+str(dict_config.camera)+"' cannot capture frame")
                    #raise
                    #Util.CloseApplication()
                else:  
                    self._log.info("Cv2 {}".format(cv2.__version__))
                    self._log.info("Width "+str(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
                    self._log.info("Height "+str(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                    self._log.info("AutoFocus "+str(camera.get(cv2.CAP_PROP_AUTOFOCUS)))
                    self._log.info("Focus "+str(camera.get(cv2.CAP_PROP_FOCUS)))
                    self._log.info("Exposure "+str(camera.get(cv2.CAP_PROP_EXPOSURE)))
                    self._log.info("Framerate "+str(camera.get(cv2.CAP_PROP_FPS)))
                    
                if not camera.isOpened():    
                    self._log.info("Alternative")
                    camera = cv2.VideoCapture(dict_config.camera)
                    
                if not camera.isOpened():
                    self._retrying = self._retrying + 1
                    self._log.error("Couldn't be opened, retry {}".format(self._retrying))
                    time.sleep(1)
                else:
                    started = True                    

            except Exception as e:
                traceback.print_exc()
                self._retrying = self._retrying + 1
                self._log.error("Retry {}.".format(self._retrying))
                time.sleep(1)
        
        self._camera = camera
        
        #print(self.camera)        
        return self
        
    def get(self):
        success, image = self._camera.read()    
        #CurrentFrame = imutils.resize(CurrentFrame, width=1944)        
        if not success:  
            self._retrying = self._retrying + 1
            self._log.error("(usb) cannot get image, retrying {}...".format(self._retrying))    
            self.create(self._config)
        return image
        
    def close(self):
        #global camera        
        if self._camera is not None:
            if self._camera.isOpened():
                self._log.info("(usb) close {}".format(self._config.source_name))
                self._camera.release()