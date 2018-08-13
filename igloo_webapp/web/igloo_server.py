from flask import (render_template, redirect, flash,
                   url_for, session, abort)
from datetime import datetime
from .run_rwmc_form import RunRWMCForm
from .fetch_data_form import FetchDataForm


class IglooServer:

    def __init__(self):
        self.db_interface = None
        self.config_io = None

    def serve_run_rwmc_form(self):
        form = RunRWMCForm()
        if form.validate_on_submit():
            job_id = self.handle_run_rwmc_form(form)
            return render_template('submit_job.html',
                                   title='Submit Job',
                                   form=form,
                                   job_id=job_id)
        return render_template('submit_job.html', title='Submit Job',
                               form=form)
    
    def handle_run_rwmc_form(self, form):
        return -1
    
    def serve_results(self):
        fetch_data_form = FetchDataForm()
        if fetch_data_form.validate_on_submit():
            return "fetch!"
        return render_template('results.html', title='Fetch Results',
                               form=fetch_data_form)
