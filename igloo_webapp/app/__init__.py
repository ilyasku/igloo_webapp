from flask import Flask
from igloo_webapp.web.igloo_server import IglooServer
# from schlechte_witze_meldesystem.persistence.sqlite_interface import SQLiteInterface
# from schlechte_witze_meldesystem.web.joke_server import JokeServer
# from schlechte_witze_meldesystem.web.config import Config
# from schlechte_witze_meldesystem.config_io import ConfigIO

import os
here = os.path.dirname(os.path.realpath(__file__))
home = home = os.path.expanduser("~")



server = IglooServer()
# server.config_io = ConfigIO()

app = Flask("IglooWebApp", template_folder=here + "/../web/templates",
            static_folder=here + "/../../static")
# app.config.from_object(Config)


from schlechte_witze_meldesystem.app import routes
