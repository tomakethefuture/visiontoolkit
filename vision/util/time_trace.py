import time
import traceback

import logging

class time_trace:
    '''
     self.time_trace.set_start_fresh("example1")
     self.time_trace.set_start("example1")
     self.time_trace.print_elapsed("example1")
     self.time_trace.print_total_elapsed("example1")
    '''
     
    def __init__(self):
        self.time_list = {}
        self.enable_print = True
        self._log = logging.getLogger("FMC.time_trace")
        
    def clear_all(self):
        self.time_list = {}
    
    def set_start(self,id_trace):
        self.time_list.update({id_trace:{"time":time.time(),"total_elapsed":self.get_total_elapsed(id_trace)}})

    def set_start_fresh(self,id_trace):
        self.time_list.update({id_trace:{"time":time.time(),"total_elapsed":0.0}})
    
    def get_start_time(self,id_trace):
        return self.time_list.get(id_trace).get("time")
     
    def get_total_elapsed(self,id_trace):   
        if self.time_list.get(id_trace) is not None:
            return self.time_list.get(id_trace).get("total_elapsed")
        else:
            return 0.0
     
    def get_elapsed(self,id_trace):
        return time.time()-self.time_list.get(id_trace).get("time")  
    
    def update_total_elapsed(self,id_trace):
        self.time_list.update({id_trace:{
                                        "time" : self.get_start_time(id_trace),
                                        "total_elapsed" : self.get_total_elapsed(id_trace)+self.get_elapsed(id_trace)
                                        }
                                })
                
    def print_elapsed(self, id_trace):
        if not self.time_list.get(id_trace) is None:
            self.update_total_elapsed(id_trace)
            if self.enable_print:
                self._log.info("id_trace {} elapsed {}".format(id_trace,self.get_elapsed(id_trace)))
        else:
            raise Exception("id_trace not found!") 
            
    def print_total_elapsed(self, id_trace):
        if self.enable_print:
            if not self.time_list.get(id_trace) is None:            
                self._log.info("id_trace {} total elapsed {}".format(id_trace,self.get_total_elapsed(id_trace)))
            else:
                raise Exception("id_trace not found!") 