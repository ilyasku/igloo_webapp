from flask import Flask
from igloo_webapp.web.job_manager import JobManager
from igloo_webapp.web.igloo_server import IglooServer

import os
here = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser("~")


def create_app(test_config=None, **kwargs):
    app = Flask(__name__, instance_relative_config=True,
                template_folder=here + "/../web/templates",
                static_folder=here + "/../static")

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'conducted_experiments.sqlite'),
        N_THREADS=2,
        DATA_FOLDER=os.path.join(app.instance_path, 'data')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from ..persistence import db
    db.init_app(app)

    return app


app = create_app()
with app.app_context():
    jm = JobManager(app.config['N_THREADS'])
    server = IglooServer(jm)

from . import routes
