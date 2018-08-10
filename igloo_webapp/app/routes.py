from igloo_webapp.app import app, server
# from igloo_webapp.app.db_connect import get_db


@app.route("/results", methods=['GET'])
def show_results():
    return server.serve_run_rwmc_form()

@app.route("/", methods=['GET', 'POST'])
def show_run_rwmc_form():
    return server.serve_run_rwmc_form()

@app.route("/admin")
def show_admin_page():
    return server.serve_admin_page()
