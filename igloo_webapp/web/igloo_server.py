from flask import (render_template, redirect, flash,
                   url_for, session, abort)
from datetime import datetime
from .run_rwmc_form import RunRWMCForm


class IglooServer:

    def __init__(self):
        self.db_interface = None
        self.config_io = None

    def serve_run_rwmc_form(self):
        form = RunRWMCForm()
        if form.validate_on_submit():
            return "valid!"
        return render_template('submit_job.html', title='Submit Job', form=form)
    
    def handle_run_rwmc_form(self):
        return "igloo_server.handle_run_rwmc_form: not implemented yet!"

    def serve_admin_page(self):
        return "Nothing here yet!"
