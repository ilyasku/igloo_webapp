import sqlite3

from flask import render_template
from datetime import datetime
import hashlib
import random
import os
from typing import List
from .run_rwmc_form import RunRWMCForm
from .fetch_data_form import FetchDataForm
from .job_manager import JobManager
from ..model.experiment import Experiment
from ..persistence.data_output_handler import get_persistent_folder_name
from ..app.db_connect import get_db

Digest = str


class IglooServer:

    def __init__(self, job_manager: JobManager):
        edb = get_db()
        self.job_manager = job_manager
        try:
            self.current_id = edb.get_maximum_id()
        except sqlite3.OperationalError:
            self.current_id = 0

    def serve_run_rwmc_form(self):
        form = RunRWMCForm()        
        if form.validate_on_submit():
            job_digest = self.handle_run_rwmc_form(form)
            return render_template('submit_job.html',
                                   title='Submit Job',
                                   form=form,
                                   job_digest=job_digest,
                                   stats=_IGLOOStats())        
        return render_template('submit_job.html', title='Submit Job',
                               form=form,
                               stats=_IGLOOStats())
    
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
        edb = get_db()
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
    
    @staticmethod
    def serve_fetch_results():
        fetch_data_form = FetchDataForm()
        if fetch_data_form.validate_on_submit():
            digest = fetch_data_form.job_digest.data
            if not _is_valid_hash(digest):
                header = "Provided hash '{}' is not valid!".format(digest)
                message = "Job hash has to consist of exactly 10 characters/numbers."
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [message]),
                                       stats=_IGLOOStats())
            e = get_db().get_experiment_by_hash_digest(digest)
            if e is None:
                header = "Job with hash '{}' not found!".format(digest)
                message =  "Either we lost track of that job or the hash you entered "
                message += "does not match the hash of your submitted job. "
                message += "Don't hesitate to contact us for help!"
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [message]),
                                       stats=_IGLOOStats())
            if e.date_finish is None:
                header = "Your job with hash '{}' is not finished!".format(digest)
                msg1 = "{}: job submitted to server".format(e.date_submit)
                if e.date_start is None:
                    msg2 = "Simulation not started yet"                    
                else:
                    msg2 = "{}: simulation started".format(e.date_start)
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [msg1, msg2]),
                                       stats=_IGLOOStats())
            header = "Job with hash '{}' finished successfully!".format(digest)
            msg0 = "Click links below to fetch data in desired format."
            msg1 = "{}: job submitted to server".format(e.date_submit)
            msg2 = "{}: simulation started".format(e.date_start)
            msg3 = "{}: simulation finished".format(e.date_finish)

            zip_file = get_persistent_folder_name(e.id_) + "/data.zip"
            if not os.path.exists(zip_file):
                return render_template('results.html', title='Fetch Results',
                                       form=fetch_data_form,
                                       message=_FetchMessage(False, header, [
                                           msg0, msg1, msg2, msg3,
                                           'But it looks like the data was deleted from the server. :(',
                                           'On our demo servers the data gets automatically deleted after a few days.'
                                       ]),
                                       digest=digest,
                                       stats=_IGLOOStats())

            file_size = _get_size_of_datazip(zip_file)
            
            return render_template('results.html', title='Fetch Results',
                                   form=fetch_data_form,
                                   message=_FetchMessage(True, header, [msg0, msg1, msg2, msg3]),
                                   digest=digest,
                                   files=[_FetchableFile('data.zip',
                                                         'Zipped raw data, collection of text files (size: {} MB)'.format(file_size))],
                                   stats=_IGLOOStats())
        return render_template('results.html', title='Fetch Results',
                               form=fetch_data_form,
                               stats=_IGLOOStats())

    @staticmethod
    def serve_authors_page():
        diggo = _Author('Diego Giraldo', 'Postdoc?',
                        'Cellular Neurobiology', 'University of G??ttingen',
                        'author_pictures/diego.png',
                        'Main paper manuscript, recording and analysis of larval data.' +
                        'Proof of concept experiments.')
        andrea = _Author('Andrea Adden', 'PhD Student',
                         'Department of Biology', 'Lund University',
                         'author_pictures/andrea.png', 'Main paper manuscript, recording and analysis of adult data.')
        ille = _Author('Ilyas Kuhlemann', 'PhD Student', 'Institute of Physical Chemistry',
                       'University of G??ttingen', 'author_pictures/ilyas.png', 'Igloo Webapp.')
        heribert = _Author('Heribert Gras', '',
                           'Cellular Neurobiology', 'University of G??ttingen',
                           'author_pictures/heribert.png', 'Formalising IGLOO model and developing the code.')
        doc_G = _Author('Bart Geurten', 'Postdoc',
                        'Cellular Neurobiology', 'University of G??ttingen',
                        'author_pictures/bart.png', 'Main paper manuscript, formalising IGLOO model and developing the code.',
                        'bart.geurten@biologie.uni-goettingen.de')
        authors = [diggo, andrea, ille, heribert, doc_G]
        return render_template('authors.html', title='Authors',
                               authors=authors)


def _is_valid_hash(h):
    if len(h) != 10:
        return False
    return True


def _get_size_of_datazip(fname: str) -> float:
    stat = os.stat(fname)
    return stat.st_size / 1.e6


class _Author:
    def __init__(self, name: str, occupation: str, institute: str,
                 employer: str,
                 picture_url: str,
                 contribution: str, contact: str=None):
        self.name = name
        self.occupation = occupation
        self.institute = institute
        self.employer = employer
        if picture_url is None:
            self.picture_url = 'author_pictures/place_holder.jpeg'
        else:
            self.picture_url = picture_url
        self.contribution = contribution
        self.contact = contact


class _FetchMessage:

    def __init__(self, success: bool, header: str, messages: List[str]):
        self.success = success
        self.header = header
        self.messages = messages


class _FetchableFile:

    def __init__(self, fname: str, label: str):
        self.fname = fname
        self.label = label


class _IGLOOStats:

    def __init__(self):
        edb = get_db()
        self.n_flies_total, self.duration_total =\
            edb.get_total_n_flies_and_duration()
        
