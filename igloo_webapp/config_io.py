import os
import json
from typing import Dict, Union

PATH_TO_CONFIG = os.path.expanduser('~/.config/igloo_webapp.json')

def write_config(path_to_data: str, n_threads: int):
    config_dict = {'path_to_data': path_to_data,
                   'n_threads': n_threads}
    json.dump(config_dict, open(PATH_TO_CONFIG, 'w'))

def read_config() -> Dict[str, Union[str, int]]:
    return json.load(open(PATH_TO_CONFIG, 'r'))
    
