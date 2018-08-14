from flask import (render_template, redirect, flash,
                   url_for, session, abort)
from datetime import datetime
from .run_rwmc_form import RunRWMCForm
from .fetch_data_form import FetchDataForm
from .job_manager import JobManager
from ..model.experiment import Experiment


Digest = str

class IglooServer:

    def __init__(self, job_manager: JobManager):
        self.db_interface = None
        self.config_io = None

    def serve_run_rwmc_form(self):
        form = RunRWMCForm()
        if form.validate_on_submit():
            job_digest = self.handle_run_rwmc_form(form)
            return render_template('submit_job.html',
                                   title='Submit Job',
                                   form=form,
                                   job_digest=job_digest)
        return render_template('submit_job.html', title='Submit Job',
                               form=form)
    
    def handle_run_rwmc_form(self, form: RunRWMCForm) -> Digest:
        e = Experiment(form.length.data,
                       form.start_pos.data,
                       form.T_min.data,
                       form.T_max.data,
                       form.T_rear.data,
                       form.duration.data,
                       form.frames_per_sec.data,
                       form.simulation_type.data,
                       form.n_flies.data)
        digest = self._start_rwmc_experiment(e)
        return digest
    
    def serve_results(self):
        fetch_data_form = FetchDataForm()
        if fetch_data_form.validate_on_submit():
            return "fetch!"
        return render_template('results.html', title='Fetch Results',
                               form=fetch_data_form)

    def _start_rwmc_experiment(self, e: Experiment) -> Digest:
        
        raise NotImplementedError()
