from flask import request, redirect, url_for, session, flash
from igloo_webapp.app import app, server
from igloo_webapp.app.db_connect import get_db


@app.route("/results", methods=['GET'])
def show_results():
    db_interface = get_db()
    return server.serve_joke_form(db_interface)

@app.route("/", methods=['GET'])
def show_run_rwmc_form():
    return server.serve_login_form()
