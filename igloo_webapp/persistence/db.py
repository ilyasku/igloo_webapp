import sqlite3
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('../persistence/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_data_folders():
    folder = current_app.config["DATA_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    for i in range(current_app.config['N_THREADS']):
        folder_name = _get_tmp_folder_name(folder, i)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)


def _get_tmp_folder_name(prefix: str, index: int) -> str:
    tmp_folder_name = prefix + "/tmp_current_simulation_{}".format(index)
    return tmp_folder_name


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo("instance_path = '{}'.".format(current_app.instance_path))
    init_db()
    click.echo('Initialized the database.')
    init_data_folders()
    click.echo('Created data folders.')
    click.echo('Somehow this command does not quit on its own ... ? Hit CTRL+C twice.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
