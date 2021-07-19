from flask import current_app


def get_tmp_folder_name(index: int) -> str:
    tmp_folder_name = (current_app.config['DATA_FOLDER']
                       + "/tmp_current_simulation_{}".format(index))
    return tmp_folder_name


def get_persistent_folder_name(id_: int) -> str:    
    return (current_app.config['DATA_FOLDER']
            + "/data_{:05d}".format(int(id_)))
