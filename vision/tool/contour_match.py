from vision.util import default
from vision.util import config
from vision.process.default_output import default_output

import logging

import os
import traceback
import cv2
import copy
import numpy as np


# Inherit default_output from flow
class output(default_output):
    def __init__(self):
        super().__init__()
        self.new_attrib = "Hello World"

class contour_match:  #tool name must same as file name
    #Type identification
    type = "contour_match"
    #Default setting structure
    default_config = {"source":"Camera1",
                      "count":1,
                      "min_area":13000,
                      "max_area":18000} 
    
    # default output after run() command started by flow    
    # default_output = {  "image":None,
                        # "score":0,
                        # "pass":0} 
    
    # logging
    _log = None         # logging
    
    # tool belong to which name
    _name_flow = None   # Belong to which flow
    _name = None        # Should be the unique name given by flow configurable by json
    
    # Coniguration
    _config = None      # Current configuration dictionary
    _path = None        # Configuration path
    
    # Output
    _output = None      # Output dictionary
  
    # Basic initialization
    def __init__(self,name_flow,name,dict_conf):
        self._log = logging.getLogger("FMC.{}.{}.show_result".format(name_flow,name))
        self._name_flow = name_flow
        self._name = name
        self._config = dict_conf
        self._path = config.get_directory_flow(name_flow)
        #self._output = copy.deepcopy(self.default_output)
        self._output = output()
        
    # for flow.py adding {"obj":self} 
    def update(self,dict_config):   
        self._config.update(dict_config)
        
    def run(self,flow,images):
        # Example of get previous tools' result output
        try :
            image = images.get(self._config['source'])
            image = cv2.GaussianBlur(image, (17, 17), 0)   
            #image = cv2.bilateralFilter(image,9,75,75)
            #img = cv.medianBlur(img,5)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret2,image = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            #image = cv2.bitwise_not(image)
            image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)            
            #image = cv2.Canny(image, 255/3, 255) 
            #high_thresh, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            #lowThresh = lowThreshRatio*high_thresh            
            #kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(3,3))
            #image = cv2.Canny(image, lowThresh, high_thresh)
            contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            count_pass = 0
            for c in contours:
                area = cv2.contourArea(c)
                print(area)
                if area > self._config['min_area'] and area < self._config['max_area']:
                    count_pass+=1
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    #print(box)
                    image = cv2.drawContours(image,[box],0,(255,255,255),2)
            #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            
            self._output.image = image
            
            if len(contours) == 1:
                self._output.passed = 1
                
            # for item in flow._flowing[self._name_flow]:
                # print(item['name'])
                # print(item['obj']._output)
            # obj = flow.get_tool_obj(self._name_flow,self._config["t"]) #get_tool_obj return None if request name of tool object not found
            #print("flow")
            #print(self._name_flow)
            #print(self._name)
            #print(self._config)
            #print(obj._name)
            #print(obj._config)
            #print(obj._output)
        except Exception as Argument:  
            #https://www.geeksforgeeks.org/how-to-log-a-python-exception/
            self._log.exception("Error occured while run()")
 
