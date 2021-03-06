from vision.util import default
from vision.util import config

import os
import traceback
import cv2
import copy

from vision.process.default_output import default_output
# Inherit default_output from flow
class output(default_output):
    def __init__(self):
        super().__init__()
        self.new_attrib = "Hello World"
        self.x=None
        self.y=None
        self.x2=None
        self.y2=None
        
class template_match:  
    _type = "template_match"
    
    default_config = {
            "source":"Camera1",
            "min":-10,
            "i_type":"file",
            "i_type_name":"a.png",
            "o_xy":0,
            "o_crop":0,
            "o_gray":0,
            "o_ori":0,
            "o_score":0}
            
    default_output = {
            "x":0,
            "y":0,
            "x2":0,
            "y2":0,
            "score":0,
            "pass":0}
    
    _name_flow = None
    _name = None
    _config = None
    _path = None
    
    # Template Match Tool variable
    _template = None
    _template_gray = None
    _output = None
  
    def __init__(self,name_flow,name,dict_conf):
        self._name_flow = name_flow
        self._name = name
        self._config = dict_conf
        self._path = config.get_directory_flow(name_flow)
        self._template = cv2.imread(os.path.join(self._path,self._config['i_type_name']))
        self._template_gray = cv2.cvtColor(self._template, cv2.COLOR_BGR2GRAY)
        self._output = output()#copy.deepcopy(self.default_output)

    def update(self,dict_config):   
        self._config.update(dict_config)
        
    def run(self,flow,images):
        #images = flow._source.get()
        image = images.get(self._config['source'])
        
        image_width,image_height=image.shape[:2]
        
        res = cv2.matchTemplate(self.to_gray(image),self._template_gray,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        self._output.x = max_loc[0]
        self._output.y = max_loc[1]
        self._output.x2 = max_loc[0] + self._template_gray.shape[1]
        self._output.y2 = max_loc[1] + self._template_gray.shape[0]
        self._output.score = max_val
        self._output.passed = max_val >= self._config['min']
        self._output.image = image
        #print(self._output)
        
        #cv2.imshow("a",image)
        #cv2.imshow("b",self._template)
        #cv2.waitKey(0)
        pass
        
    #def output(self):
    #    return self._output
        
    def to_gray(self,image):
        # Convert to grayscale. 
        if len(image.shape)==3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        else:
            image = image
        return image     
        
    # def _run(self,image,dict_config):
        # try:
            # w = TemplateImage.shape[1]
            # h = TemplateImage.shape[0]            

            # res = cv2.matchTemplate(self.to_gray(CurrentImage),self.to_gray(TemplateImage),cv2.TM_CCOEFF_NORMED)
            
            # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)    

            # top_left = max_loc
            # top_val = max_val
            # bottom_right = (top_left[0] + w, top_left[1] + h)

            # croppedImage = CurrentImage[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
            # originalCropped = croppedImage
            # return res,top_left,bottom_right,top_val,croppedImage,originalCropped  
        # except:
            # traceback.print_exc()
            # return None,(1,1),(2,2),0,CurrentImage,TemplateImage