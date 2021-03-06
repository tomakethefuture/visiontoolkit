import logging

from vision.util import default
from vision.util import config
from vision.util import structure



import copy

class flow:

    _name = None        # not finalized yet
    
    _log = None         # Logger "FMC.flow"
    
    _flow = None        # read from flow_name.json
    _current = None     # dictionary _flow added object tool {"obj":tool_name}
        
    _source = None      # collection of image/camera sources
    
    _images = None      # current images from source.get()
    
    def __init__(self):
        self._log = logging.getLogger("FMC.flow")
        self._name = ""
    
    # add link to collection of image/camera sources
    def update_source(self,source):
        self._source = source
    
    def load(self,flow_name):
        # unload if _flow and _current is loaded
        self.unload()
        
        self._name = flow_name  # not finalized yet      
        
        self._flow = config.get_flow(flow_name,{flow_name:[]})    
        
        self._current = copy.deepcopy(self._flow)
        
        for item in self._current[flow_name]:
            item.update({"obj":self.load_tool(item,flow_name)})
            #print(item)
            #print(item["obj"]._name)
        
    # sub routine to dynamically load and return initialized tool object
    def load_tool(self,val_dict,flow_name):
        exec("from vision.tool.{0} import {0}".format(val_dict['tool']))
        dict_config = copy.deepcopy(eval("{}.default_config".format(val_dict['tool'])))
        dict_config = config.get_config_tool(self._name,val_dict['name'],val_dict['tool'],dict_config)
        obj_tool = eval("{}(flow_name,val_dict['name'],dict_config)".format(val_dict['tool']))
        return obj_tool
    
    def unload(self):
        self._flow = {}
        self._current = {}
    
    # to be use after flow was edited
    def reload(self,flow_name=None):
        if flow_name is None:
            flow_name = self._name
            
        self._current = copy.deepcopy(self._flow)
        
        for item in self._current[flow_name]:
            item.update({"obj":self.load_tool(item,flow_name)})
    
    # return previous tool's object
    def get_tool_obj(self,name_flow,name):
        for item in self._current[name_flow]:
            if item['name'] == name:
                return item['obj']    
    
    # add new tool into dictionary _flow
    def add_tool(self,name,name_tool,flow_name=None):
        if flow_name is None:
            flow_name = self._name
            
        self._flow[flow_name].insert(len(self._flow[flow_name]),{"name":name,"tool":name_tool})
    
    # save dictionary _flow to flow_name.json
    def save(self,flow_name=None):
        if flow_name is None:
            flow_name = self._name
            
        config.save_flow(flow_name,self._flow)
        for item in self._current[flow_name]:
            config.save_config_tool(flow_name,item['name'],item['tool'],item['obj']._config)
    
    # run all tool according to config setting
    def run(self):
        try:
            self._images = self._source.get()
            for item in self._current[self._name]:
                #images = source.get()
                item['obj'].run(self,self._images)
        except Exception as Argument:  
            #https://www.geeksforgeeks.org/how-to-log-a-python-exception/
            self._log.exception("Error occured while run()")
    
    def get_structure_flow(self):        
        return {"name":"",
                "tool":""}