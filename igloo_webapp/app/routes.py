from flask import send_from_directory, render_template
from igloo_webapp.app import app, server, read_config
from igloo_webapp.persistence.data_output_handler import get_persistent_folder_name
from igloo_webapp.persistence.experiments_database import ExperimentsDatabase
# from igloo_webapp.app.db_connect import get_db


@app.route("/results", methods=['GET', 'POST'])
def show_fetch_results():
    return server.serve_fetch_results()

@app.route("/submit-job", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def show_run_rwmc_form():
    return server.serve_run_rwmc_form()

@app.route("/admin")
def show_admin_page():
    return server.serve_admin_page()

@app.route("/fetch/<digest>/<fname>")
def fetch(digest: str, fname: str):
    id_ = ExperimentsDatabase().get_experiment_by_hash_digest(digest).id_
    folder_name = get_persistent_folder_name(id_)
    return send_from_directory(folder_name, fname, as_attachment=True)

@app.route("/not-published-yet")
def show_not_published():
    return app.send_static_file('not_published.html')

@app.route("/impressum")
def show_impressum():
    return render_template("impressum.html")

@app.route("/authors")
def show_authors():
    return server.serve_authors_page()

@app.route("/doc")
def show_igloo_doc():
    return app.send_static_file('doc/igloo_documentation_0_1.pdf')
