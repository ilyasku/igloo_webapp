import os
import json
from typing import Dict, Union

PATH_TO_CONFIG = os.path.expanduser('~/.config/igloo_webapp.json')
ROOT_PATH_TO_CONFIG = '/etc/igloo_webapp.json'

def write_config(path_to_data: str, n_threads: int,
                 path_to_static: str, path_to_templates: str):
    config_dict = {'path_to_data': path_to_data,
                   'n_threads': n_threads,
                   'path_to_static': path_to_static,
                   'path_to_templates': path_to_templates}
    
    path_to_config = PATH_TO_CONFIG
        
    json.dump(config_dict, open(path_to_config, 'w'))

def read_config() -> Dict[str, Union[str, int]]:        
    try:
        conf = json.load(open(ROOT_PATH_TO_CONFIG, 'r'))
    except (PermissionError, FileNotFoundError):
        conf = json.load(open(PATH_TO_CONFIG, 'r'))
    return conf
    
