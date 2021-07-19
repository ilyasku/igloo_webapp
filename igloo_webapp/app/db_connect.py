from flask import g
from igloo_webapp.persistence.experiments_database import ExperimentsDatabase


def connect_db():
    db_interface = ExperimentsDatabase()
    return db_interface


def get_db():
    if not hasattr(g, 'db_interface'):
        g.db_interface = connect_db()
    return g.db_interface
