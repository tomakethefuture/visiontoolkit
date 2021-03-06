import logging
from vision.util import config
from vision.util import default
from vision.util import structure


class configure:
    
    def __init__(self):
        self._log = logging.getLogger("FMC.config.configure")
        self._vision = config.get_config(default.FILE_NAME_CONFIG_VISION,structure.CONFIG_VISION)
        self._log.info('vision loaded')