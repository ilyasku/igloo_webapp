from flask import (render_template, redirect, flash,
                   url_for, session, abort)
from datetime import datetime
from .run_rwmc_form import RunRWMCForm


class IglooServer:

    def __init__(self):
        self.db_interface = None
        self.config_io = None

    def serve_run_rwmc_form(self, db_interface):
        return "igloo_server.serve_run_rwmc_form: not implemented yet!"
    
    def handle_run_rwmc_form(self, form_dict, db_interface):
        return "igloo_server.handle_run_rwmc_form: not implemented yet!"
