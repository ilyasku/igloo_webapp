import sqlite3
import os
import click
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
    date_start text,
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

@click.command()
@click.argument('path-to-data')
@click.option('--n-threads', '-n', default=4, type=int)
@click.option('--path-to-static', '-s', default='/var/www/igloo_webapp/static')
@click.option('--path-to-templates', '-t', default='/var/www/igloo_webapp/templates')
def main(path_to_data, n_threads, path_to_static, path_to_templates):
    write_config(path_to_data, n_threads, path_to_static, path_to_templates)
    _create_experiments_database(path_to_data + '/conducted_experiments.sqlite')
    _create_current_simulations_folders(path_to_data, n_threads)

if __name__ == '__main__':
    main()
