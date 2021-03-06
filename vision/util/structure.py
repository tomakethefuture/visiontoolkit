# Setting for vision system
CONFIG_VISION  = {  'source':["Camera1"],    
                    'startup':'product',
                    'selected_camera':'Camera1',
                    'selected_flow':'Flow1',
                    'preview_size':[100,100],
                    'color_fail':'red',
                    'enable_serial':False,
                    'enable_edit':True,
                    'zoom':"fit"
                    }


# Setting for cameras
SOURCE_CAMERA = {   'source_type':'camera',
                    'camera_type':'usb',
                    'camera':'0',
                    'camera_framerate':None,
                    'camera_exposure':None,
                    'camera_focus':None,
                    'camera_V4L2_format':"MJPG",
                    'camera_directshow':True,
                    'camera_resolution_width':None,
                    'camera_resolution_height':None            
                    }

SOURCE_HTTP = { 'source_type':'http'}

FLOW = {"Flow1":[]}