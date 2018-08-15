from flask import Flask
from igloo_webapp.web.job_manager import JobManager
from igloo_webapp.web.igloo_server import IglooServer
from igloo_webapp.web.config import Config
from igloo_webapp.config_io import read_config

import os
here = os.path.dirname(os.path.realpath(__file__))
home = home = os.path.expanduser("~")



jm = JobManager(read_config()['n_threads'])
server = IglooServer(jm)
# server.config_io = ConfigIO()

app = Flask("IglooWebApp", template_folder=here + "/../web/templates",
            static_folder=here + "/../../static")
app.config.from_object(Config)


from igloo_webapp.app import routes
