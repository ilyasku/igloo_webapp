import sqlite3
import os
from igloo_webapp.config_io import write_config



def _create_experiments_database(path_to_db):
    if os.path.exists(path_to_db):
        print("file '" + path_to_db + "' already exists")
        read = input("do you want to overwrite it? [y/N] ")
        if not read.lower() == "y":
            return
        os.remove(path_to_db)
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()    

    create_string = """CREATE TABLE experiments (
    _id integer PRIMARY KEY AUTOINCREMENT,
    hash text NOT NULL,
    length real NOT NULL,
    start_pos real NOT NULL,
    T_min real NOT NULL,
    T_max real NOT NULL,
    T_rear real NOT NULL,
    duration real NOT NULL,
    frames_per_sec real NOT NULL,
    simulation_type text NOT NULL,
    n_flies integer NOT NULL,
    date_submit text NOT NULL,
    date_start text NOT NULL,
    date_finish text)
    """
    cursor.execute(create_string)
    connection.commit()

def _create_current_simulations_folders(path_to_data: str, n_threads: int):
    for i in range(n_threads):
        folder_name = _get_tmp_folder_name(path_to_data, i)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

def _get_tmp_folder_name(prefix: str, index: int) -> str:
    tmp_folder_name = prefix + "/tmp_current_simulation_{}".format(index)
    return tmp_folder_name

def main():
    import sys
    if '--n-threads' in sys.argv:
        n_threads = int(sys.argv[sys.argv.index('--n-threads') + 1])
    else:
        n_threads = int(input("Number of threads igloo can use: "))
    if '--path-to-data' in sys.argv:
        path_to_data = sys.argv[sys.argv.index('--path-to-data')+1]
    else:
        path_to_data = input("Folder to store data in: ")
    if '--path-to-templates' in sys.argv:
        path_to_templates = sys.argv[sys.argv.index('--path-to-templates')+1]
    else:
        path_to_templates = input("Path to HTML templates: ")
    if '--path-to-static' in sys.argv:
        path_to_static = sys.argv[sys.argv.index('--path-to-static')+1]
    else:
        path_to_static = input("Path to static files (css, js, images): ")
    write_config(path_to_data, n_threads, path_to_static, path_to_templates)
    _create_experiments_database(path_to_data + '/conducted_experiments.sqlite')
    _create_current_simulations_folders(path_to_data, n_threads)

if __name__ == '__main__':
    main()
