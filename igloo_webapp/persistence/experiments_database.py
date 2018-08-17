import sqlite3
from ..model.experiment import Experiment
from ..config_io import read_config


class ExperimentsDatabase:

    def __init__(self):
        self.path_to_db = read_config()['path_to_data'] + '/conducted_experiments.sqlite'
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()
        self.cursor.arraysize = 30

    def get_experiment_by_hash_digest(self, digest: str) -> Experiment:
        """
        Query database for an entry with matching digest.
        @param digest shake_128 digest as hex, created from experiment's id (starting at 0,
                      incremented for each experiment), limited to 8 digits. 
        """
        fetch_string = "SELECT * FROM experiments WHERE hash=?"
        self.cursor.execute(fetch_string, (digest,))
        experiment_tuple = self.cursor.fetchone()
        if experiment_tuple is None:
            return None
        return Experiment.from_database_tuple(experiment_tuple)
        
    def insert_experiment(self, experiment: Experiment):
        insert_string = """INSERT INTO experiments 
        (_id, hash, length, start_pos, T_min, T_max, T_rear, duration, 
         frames_per_sec, simulation_type, n_flies, date_submit, date_start,
         date_finish)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(insert_string, experiment.to_database_tuple())
        self.connection.commit()

    def set_date_start(self, experiment_id: int, date_start: str):
        update_string = "UPDATE experiments SET date_start = ? WHERE _id = ?"
        self.cursor.execute(update_string, (date_start, experiment_id))
        self.connection.commit()
        
    def set_date_finish(self, experiment_id: int, date_finish: str):
        update_string = "UPDATE experiments SET date_finish = ? WHERE _id = ?"
        self.cursor.execute(update_string, (date_finish, experiment_id))
        self.connection.commit()
        
    def get_maximum_id(self) -> int:
        select_string = """SELECT max(_id) FROM experiments"""
        self.cursor.execute(select_string)        
        id_tuple = self.cursor.fetchone()
        if id_tuple[0] is None:
            return -1
        return id_tuple[0]
        
    def hash_is_already_in_db(self, digest: str) -> bool:
        self.cursor.execute("SELECT _id FROM experiments WHERE hash = ?", (digest,))
        return_tuple = self.cursor.fetchone()
        if return_tuple is None:
            return False
        return True
        
