import logging


import json
import os
import sys

import pandas

from vision.util import default

_log = logging.getLogger("FMC.config")

class obj_from_dict(dict):
    def __getattr__(self, name):
        return self.__getitem__(name)

class Dict2Obj(dict):
    #https://www.blog.pythonlibrary.org/2014/02/14/python-101-how-to-change-a-dict-into-a-class/
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])
    def __repr__(self):
        """"""
        return "{}".format(self.__dict__)
        
class obj_from_json_str:
    def __init__(self,data):
        self.__dict__ = json.loads(data)

def dict_to_obj(dic):
    return Dict2Obj(dic)
    
def get_working_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.getcwd()
        
def write_to_json(full_path,obj):
    with open(full_path, 'w') as fp:
        json.dump(obj, fp,indent=4,sort_keys=True,ensure_ascii=False)

def read_from_json(full_path):
    with open(full_path, 'r') as fp:
        return Dict2Obj(json.load(fp))
        
def read_update_from_json(full_path,dictionary):
    with open(full_path, 'r') as fp:   
        #print(dictionary)
        #print(json.load(fp))
        a = json.load(fp)
        #print(a)
        #print(type(a))
        dictionary.update(a)
        #print(dictionary)
        #dictionary.update(json.load(fp))
        return Dict2Obj(dictionary)

def read_dict_from_json(full_path,dictionary=None):
    with open(full_path, 'r') as fp:
        a = json.load(fp)
        if dictionary is not None:
            dictionary.update(a)
        return dictionary


# FLOW Directory
def get_directory_flow(flow_name):
    return os.path.join(get_working_path(),default.PATH_FLOW,flow_name)
    
# FLOW List
def get_flow(flow_name,dic):
    path_flow = get_directory_flow(flow_name)
   
    flow_filename = flow_name + ".json"
   
    full_path = os.path.join(path_flow,flow_filename)
     
    if not os.path.exists(path_flow):
        os.makedirs(path_flow)
        
    if not os.path.exists(full_path):
        #dic.update({"name":flow_name})
        write_to_json(full_path,dic)
        _log.info("flow file {} write.".format(flow_filename))
        
    if os.path.exists(full_path):
        dic = read_dict_from_json(full_path,dic)
        _log.info("flow file {} loaded.".format(flow_filename))
        
    return dic
    
# FLOW Save   
def save_flow(flow_name,dic):
    path_flow = os.path.join(get_working_path(),default.PATH_FLOW,flow_name)
   
    flow_filename = flow_name+".json"
   
    full_path =os.path.join(path_flow,flow_filename)
     
    if not os.path.exists(path_flow):
        os.makedirs(path_flow)
    
    write_to_json(full_path,dic)
    _log.info("flow file {} write.".format(flow_filename))
    
    return True
 
def get_config_tool(name_flow,name,name_tool,dic):
    path_flow = os.path.join(get_working_path(),default.PATH_FLOW,name_flow)
   
    filename_tool = "{}_{}_{}.json".format(name_flow,name,name_tool)
   
    full_path =os.path.join(path_flow,filename_tool)
     
    if not os.path.exists(path_flow):
        os.makedirs(path_flow)
        
    if not os.path.exists(full_path):
        write_to_json(full_path,dic)
        _log.info("{} {} config write.".format(name_flow,name_tool))
        
    if os.path.exists(full_path):
        dic = read_dict_from_json(full_path,dic)
        _log.info("{} {} config loaded.".format(name_flow,name_tool))
        
    return dic
    
def save_config_tool(name_flow,name,name_tool,dic):
    path_flow = os.path.join(get_working_path(),default.PATH_FLOW,name_flow)
   
    filename_tool = "{}_{}_{}.json".format(name_flow,name,name_tool)
   
    full_path =os.path.join(path_flow,filename_tool)
     
    if not os.path.exists(path_flow):
        os.makedirs(path_flow)
        
    write_to_json(full_path,dic)
    _log.info("{} {} config write.".format(name_flow,name_tool))        
        
    return True

def get_config(config_filename,dic):
    '''
    input working directory file path
    input default dictionary
    return Dict2Obj
    '''

    config_path = os.path.join(get_working_path(),default.PATH_CONFIG)
   
    full_path =os.path.join(config_path,config_filename)
    
    config_obj = dict_to_obj(dic)    
    
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        
    if not os.path.exists(full_path):
        write_to_json(full_path,vars(config_obj))
        _log.info("default config file {} write.".format(config_filename))
        
    if os.path.exists(full_path):
        config_obj = read_update_from_json(full_path,dic)
        _log.info("config file {} loaded.".format(config_filename))
        
    return config_obj

def set_config(config_filename,config_obj):
    config_path = os.path.join(get_working_path(),default.PATH_CONFIG)
   
    full_path =os.path.join(config_path,config_filename)
     
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        
    write_to_json(full_path,vars(config_obj))
    _log.info("(configuration) Config file {} write".format(config_filename))
        
def get_dataframe(dataframe_filename,df):
    data_path = os.path.join(get_working_path(),default.PATH_DATA)
    
    full_path = os.path.join(data_path,dataframe_filename)
        
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        
    if not os.path.exists(full_path):
        df.to_pickle(full_path)
        _log.info("(configuration) Dataframe file {} write".format(dataframe_filename))
        
    if os.path.exists(full_path):
        datatable = pandas.read_pickle(full_path)
        _log.info("(configuration) Dataframe file {} loaded".format(dataframe_filename))
    else:
        raise Exception("Dataframe file not found! : {}".format(full_path))  
        
    return datatable
    
def set_dataframe(dataframe_filename,df):
    data_path = os.path.join(get_working_path(),default.PATH_DATA)
    
    full_path = os.path.join(data_path,dataframe_filename)
        
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        
    df.to_pickle(full_path)
    _log.info("(configuration) Dataframe file {} write".format(dataframe_filename))
    
def get_product():
    data_path = os.path.join(get_working_path(),default.PATH_DATA)
    list_data = []
    for filename in os.listdir(data_path):
    #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        if filename.endswith(".pkl"): 
            # print(os.path.join(directory, filename))
            #https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
            list_data.append(os.path.splitext(filename)[0])
        else:
            pass
    list_data.sort()
    return list_data

def get_source():
    data_path = os.path.join(get_working_path(),default.PATH_CONFIG)
    list_data = []
    for filename in os.listdir(data_path):
    #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        if filename.startswith("source"): 
            # print(os.path.join(directory, filename))
            #https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
            list_data.append(os.path.join(directory, filename))
        else:
            pass
    list_data.sort()
    return list_data
   
def get_pass_fail():
    
    log_path = os.path.join(get_working_path(),default.PATH_LOG)
    
    full_path =os.path.join(log_path,default.FILE_NAME_LOG_PASS_FAIL)
    
    pass_fail_obj = dict_to_obj(structure.pass_fail) 
    
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        
    if not os.path.exists(full_path):
        write_to_json(full_path,vars(pass_fail_obj))
        _log.info("(configuration) default pass fail file {} write".format(default.FILE_NAME_LOG_PASS_FAIL))
        
    if os.path.exists(full_path):
        pass_fail_obj = read_from_json(full_path)
        _log.info("(configuration) pass fail file {} loaded".format(default.FILE_NAME_LOG_PASS_FAIL))
        
    return pass_fail_obj
        
def set_pass_fail(obj):
    log_path = os.path.join(get_working_path(),default.PATH_LOG)
    
    full_path =os.path.join(log_path,default.FILE_NAME_LOG_PASS_FAIL)

    if not os.path.exists(log_path):
        os.makedirs(log_path)
        
    write_to_json(full_path,vars(obj))
    _log.info("(configuration) pass fail file {} write".format(default.FILE_NAME_LOG_PASS_FAIL)) 