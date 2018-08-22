from ..config_io import read_config

def get_tmp_folder_name(index: int) -> str:
    tmp_folder_name = read_config()['path_to_data'] + "/tmp_current_simulation_{}".format(index)
    return tmp_folder_name
    
def get_persistent_folder_name(id_: int) -> str:    
    return read_config()['path_to_data'] + "/data_{:05d}".format(int(id_))
