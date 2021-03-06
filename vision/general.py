import logging

from vision.image.source import source

from vision.process.flow import flow

from vision.ui.gui import gui
import vision.ui.edit as edit

from vision.util import constant
from vision.util import default
from vision.util import config
from vision.util import structure
from vision.util.time_trace import time_trace

from vision.setting.configure import configure

import cv2

class main:
    #Config
    _log = None
    _configure = None
    _config_vision = None
    _source = None
    _flow = None
    _time_trace = None
    
    _ui = None


    def __init__(self):
        # logging
        logging.basicConfig(level=logging.DEBUG)        
        self._log = logging.getLogger("FMC")
        self._log.info('initialization')
        
        # stop watch
        self._time_trace = time_trace()
        
        self._configure = configure()
                                        
        self._source = source()        
        self._source.load(self._configure._vision.source)
        
        self._flow = flow()
        self._flow.load(self._configure._vision.selected_flow)
        self._flow.update_source(self._source)
        #self._flow.run()
        #self._flow.add_tool("hello world 333","template_match")
        #self._flow.save()
        #self._flow.add_tool("grant result","show_result")
        self._flow.reload()
        
        #self._ui = gui(self)
        self._ui = edit.main(self)
        
        self._source.close()

        
    def detect(self):
        self._time_trace.set_start_fresh("1")
        self._flow.run()
        self._time_trace.print_elapsed("1")   
        
        
        