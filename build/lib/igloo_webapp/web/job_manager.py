import time
import datetime
import shutil
import os
import glob
import zipfile
from multiprocessing import Process, Queue
import matplotlib
matplotlib.use('TKAgg')
from IGLOO import IGLOO
from ..model.experiment import Experiment
from ..config_io import read_config
from ..persistence.experiments_database import ExperimentsDatabase
from ..persistence.data_output_handler import get_tmp_folder_name, get_persistent_folder_name



class JobManager:

    def __init__(self, n_processes: int):
        self.n_processes = n_processes
                
        self.waiting_jobs = Queue()

        for i in range(self.n_processes):
            Process(target=_worker, args=(self.waiting_jobs, i)).start()

    def put_job(self, e: Experiment):
        self.waiting_jobs.put(e)
        
    def __del__(self):
        for i in range(self.n_processes):
            self.waiting_jobs.put('STOP')
    
def _worker(in_queue: Queue, process_index: int):
    for e in iter(in_queue.get, 'STOP'):
        _perform_simulation_and_update_database(e, process_index)
        _move_data_from_tmp_to_persistent_folder(e.id_, process_index)        

def _perform_simulation_and_update_database(e: Experiment, index: int):
    edb = ExperimentsDatabase()
    
    rwmc = IGLOO(**(e.to_kwargs_dict_for_RWMC()))
    e.date_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    edb.set_date_start(e.id_, e.date_start)    
    
    rwmc.simulateFlyPopulation(e.n_flies)
    
    tmp_folder_name = get_tmp_folder_name(index)
    if not os.path.isdir(tmp_folder_name):
        os.mkdir(tmp_folder_name)
    rwmc.save4TXTPopulation(tmp_folder_name)

    files = glob.glob(tmp_folder_name + "/*")
    with zipfile.ZipFile(tmp_folder_name + "/data.zip", 'w') as zfile:
        for f in files:
            zfile.write(f, arcname=os.path.split(f)[1])
    for f in files:
        os.remove(f)    
    
    e.date_finish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    edb.set_date_finish(e.id_, e.date_finish)

def _move_data_from_tmp_to_persistent_folder(id_: int, index: int):
    tmp_folder = get_tmp_folder_name(index)
    pers_folder = get_persistent_folder_name(id_)
    shutil.move(tmp_folder, pers_folder)
    os.mkdir(tmp_folder)
    
    
