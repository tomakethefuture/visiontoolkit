from vision.util import default
from vision.util import config

import logging

import os
import traceback
import cv2
import copy



class show_result:  #tool name must same as file name
    #Type identification
    type = "show_result"
    
    #Default structure
    default_config = {"t":"hello world"} # default setting
            
    default_output = {} # default output after run() command started by flow
    
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
        self._output = copy.deepcopy(self.default_output)
        
    # for flow.py adding {"obj":self} 
    def update(self,dict_config):   
        self._config.update(dict_config)
        
    def run(self,flow,images):
        # Example of get previous tools' result output
        try :
            for item in flow._current[self._name_flow]:
                print(item['name'])
                print(item['obj']._output)
            obj = flow.get_tool_obj(self._name_flow,self._config["t"]) #get_tool_obj return None if request name of tool object not found
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
 
