class Experiment:

    n_conducted_experiments = 0
    
    def __init__(self, length: float, start_pos: float,
                 T_min: float, T_max: float, T_rear: float,
                 duration: float, frames_per_sec: float,
                 simulation_type: str,
                 n_flies: int):

        self.id_ = None
        self.digest = None
        self.date_start = None
        self.date_finish = None
        self.length = length
        self.start_pos = start_pos
        self.T_min = T_min
        self.T_max = T_max
        self.T_rear = T_rear
        self.duration = duration
        self.frames_per_sec = frames_per_sec
        self.simulation_type = simulation_type
        self.n_flies = n_flies

    def to_database_tuple(self):
        t = (self.id_, self.digest,
             self.length, self.start_pos,
             self.T_min, self.T_max, self.T_rear,
             self.duration, self.frames_per_sec,
             self.simulation_type, self.n_flies,
             self.date_start, self.date_finish)
        return t

    def to_kwargs_dict_for_RWMC(self):
        kwargs = {'startPos': self.start_pos,
                  'gradientExt': (self.T_min, self.T_max),
                  'gradientDist': self.length,
                  'walkDur': self.duration,
                  'rearingT': self.T_rear,
                  'sps': self.frames_per_sec,
                  'simulationType': self.simulation_type}
        return kwargs
    
    @staticmethod
    def from_database_tuple(experiment_tuple):
        e = Experiment(experiment_tuple[2], experiment_tuple[3],
                       experiment_tuple[4], experiment_tuple[5],
                       experiment_tuple[6], experiment_tuple[7],
                       experiment_tuple[8], experiment_tuple[9],
                       experiment_tuple[10])
        e.id_ = experiment_tuple[0]
        e.digest = experiment_tuple[1]
        e.date_start = experiment_tuple[11]
        e.date_finish = experiment_tuple[12]
        return e
    
