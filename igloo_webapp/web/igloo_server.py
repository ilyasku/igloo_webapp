from flask import (render_template, redirect, flash,
                   url_for, session, abort)
from datetime import datetime
import hashlib
import random
from typing import List
from .run_rwmc_form import RunRWMCForm
from .fetch_data_form import FetchDataForm
from .job_manager import JobManager
from ..model.experiment import Experiment
from ..persistence.experiments_database import ExperimentsDatabase


Digest = str

class IglooServer:

    def __init__(self, job_manager: JobManager):
        edb = ExperimentsDatabase()
        self.job_manager = job_manager
        self.current_id = edb.get_maximum_id()

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
        edb = ExperimentsDatabase()
        self.current_id += 1
        e.id_ = self.current_id
        now = datetime.now()
        e.date_submit = now.strftime("%Y-%m-%d %H:%M:%S")
        m = hashlib.sha256()
        m.update(str(e.id_ * now.microsecond).encode())
        d = m.hexdigest()[:10]
        while edb.hash_is_already_in_db(d):
            m.update(str(random.randint).encode())
            d = m.hexdigest()[:10]
        e.digest = d
        edb.insert_experiment(e)
        self.job_manager.put_job(e)
        
        return e.digest
    
    def serve_fetch_results(self):
        fetch_data_form = FetchDataForm()
        if fetch_data_form.validate_on_submit():
            digest = fetch_data_form.job_digest.data
            if not _is_valid_hash(digest):
                header = "Provided hash '{}' is not valid!".format(digest)
                message = "Job hash has to consist of exactly 10 characters/numbers."
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [message]))
            e = ExperimentsDatabase().get_experiment_by_hash_digest(digest)
            if e is None:
                header = "Job with hash '{}' not found!".format(digest)
                message =  "Either we lost track of that job or the hash you entered "
                message += "does not match the hash of your submitted job. "
                message += "Don't hesitate to contact us for help!"
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [message]))
            if e.date_finish is None:
                header = "Your job with hash '{}' is not finished!".format(digest)
                msg1 = "{}: job submitted to server".format(e.date_submit)
                if e.date_start is None:
                    msg2 = "Simulation not started yet"                    
                else:
                    msg2 = "{}: simulation started".format(e.date_start)
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [msg1, msg2]))
            header = "Job with hash '{}' finished successfully!".format(digest)
            msg0 = "Click links below to fetch data in desired format."
            msg1 = "{}: job submitted to server".format(e.date_submit)
            msg2 = "{}: simulation started".format(e.date_start)
            msg3 = "{}: simulation finished".format(e.date_finish)
            return render_template('results.html', title='Fetch Results',
                                   form=fetch_data_form,
                                   message=_FetchMessage(True, header, [msg0, msg1, msg2, msg3]),
                                   digest=digest,
                                   files=[_FetchableFile('out.json',
                                                         'dummy file (size: 124.2 MB)!')])
        return render_template('results.html', title='Fetch Results',
                               form=fetch_data_form)

def _is_valid_hash(h):
    if len(h) != 10:
        return False
    return True
    
class _FetchMessage:

    def __init__(self, success: bool, header: str, messages: List[str]):
        self.success = success
        self.header = header
        self.messages = messages

class _FetchableFile:

    def __init__(self, fname: str, label: str):
        self.fname = fname
        self.label = label
