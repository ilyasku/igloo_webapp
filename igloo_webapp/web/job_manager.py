import time
import datetime
import shutil
import os
from multiprocessing import Process, Queue
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

class DummyRWMC:

    def __init__(self, startPos=25.,gradientExt=(12.,32.),gradientDist=50.,
                 walkDur=300.,rearingT=25.,sps=50,piloting=0,optT=21.0,
                 pilotNoise=0.25,simulationType ='interpolate'):

        # set values to inputs or defaults
        self.startPosition  = startPos          # start position of the animal [mm]
        self.position       = startPos          # current position of the animal [mm]
        self.gradientExt    = gradientExt       # cold and hot max values for the gradient [°C]
        self.gradientDist   = gradientDist      # length of the gradient [mm]
        self.sps            = sps               # samples per second 
        self.piloting       = piloting          # if piloting via arista sensors is turned on
        self.optT           = optT              # optimal temperature needed for piloting        
        self.walkDur        = walkDur           # duration of the simulation [s]
        self.rearingT       = rearingT          # temperature it which the animal was reared [°C]
        self.pilotNoise     = pilotNoise        # piloting sensory noise
        self.simulationType = simulationType    # either 'onData' or 'interpolation'

    def simulateFlyPopulation(self, n):
        time.sleep(n)

    def write_dummy_file(self, fname):
        import json
        json.dump({'start_pos': self.startPosition, 'simulation_type': self.simulationType},
                  open(fname, 'w'))
    
def _worker(in_queue: Queue, process_index: int):
    for e in iter(in_queue.get, 'STOP'):
        _perform_simulation_and_update_database(e, process_index)
        _move_data_from_tmp_to_persistent_folder(e.id_, process_index)        

def _perform_simulation_and_update_database(e: Experiment, index: int):
    edb = ExperimentsDatabase()
    
    rwmc = DummyRWMC(**(e.to_kwargs_dict_for_RWMC()))
    e.date_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    edb.insert_experiment(e)    
    
    rwmc.simulateFlyPopulation(e.n_flies)
    
    tmp_folder_name = get_tmp_folder_name(index)
    if not os.path.isdir(tmp_folder_name):
        os.mkdir(tmp_folder_name)
    fname = tmp_folder_name + "/out.json"
    rwmc.write_dummy_file(fname)
    
    e.date_finish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    edb.set_date_finish(e.id_, e.date_finish)

def _move_data_from_tmp_to_persistent_folder(id_: int, index: int):
    tmp_folder = get_tmp_folder_name(index)
    pers_folder = get_persistent_folder_name(id_)
    shutil.move(tmp_folder, pers_folder)
    os.mkdir(tmp_folder)
    
    
