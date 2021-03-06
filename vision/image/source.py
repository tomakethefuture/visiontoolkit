import concurrent.futures

import logging

from vision.util import constant
from vision.util import default
from vision.util import config
from vision.util import structure

from vision.image.cameras.camera import camera

class source:
    _sources = None
    _futures = None
    _log = None
    
    def __init__(self):
        self._log = logging.getLogger("FMC.source")
        self._futures = concurrent.futures.ThreadPoolExecutor()
        self._sources = {}
        pass
        
    def load(self,dict_source):
        self._log.info('load')  
        
        list_config_source = {}
        for name in dict_source:
            structure_config = structure.SOURCE_CAMERA.copy()
            structure_config.update({"source_name":name})
            list_config_source.update({name:config.get_config("source_{}.json".format(name),structure_config)})
        
        #print(list_config_source)
        
        for key, dict in list_config_source.items():
            if dict.source_type == "camera":
                if dict.camera_type == "usb":
                    self._sources.update({key:camera().create(dict)})
                    
                    
    def get(self,source_name = None):
        if source_name is None:
            all_image = {}
            #with concurrent.futures.ThreadPoolExecutor() as executor: #EXPERIMENTAL change on 2020-08-13 v3.3.5-Dev
            future ={}            
            for name,val_source in self._sources.items():
                #cam = cam.get("camera")
                if val_source is not None:
                    future.update({name:self._futures.submit(val_source.get)})                    
                else:                    
                    raise Exception("Source name \"{}\" not found!".format(name))   
            
            #all_image = future
            for n,(name,f) in enumerate(future.items()):
                all_image.update({name:f.result()})             
                
            if len(all_image)>0:
                return all_image
            else:
                raise Exception("Not image from source!")  
        else:
            return self._sources.get(source_name).get()
    
    def close(self,source_name = None):
        for name,val_source in self._sources.items():
            val_source.close()
        