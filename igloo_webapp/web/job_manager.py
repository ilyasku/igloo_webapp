import time
import datetime
from multiprocessing import Process, Queue
from ..model.experiment import Experiment



class JobManager:

    def __init__(self, n_processes: int):
        self.n_processes = n_processes
                
        self.waiting_jobs = Queue()
        self.finished_jobs = Queue()

        for i in range(self.n_processes):
            Process(target=worker, args=(self.waiting_jobs, self.finished_jobs)).start()

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
    
def _worker(in_queue: Queue, out_queue):
    for e in iter(in_queue.get, 'STOP'):
        rwmc = DummyRWMC(**(e.to_kwargs_dict_for_RWMC()))
        rwmc.simulateFlyPopulation(e.n_flies)
        out_queue.put((e.id_, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
