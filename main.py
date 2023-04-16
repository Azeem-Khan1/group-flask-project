# import "packages" from flask
import model_users
from flask import render_template  # import render_template from "public" flask libraries
# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from apis.twoapi import app_api # blueprint import api definition
#from apis.covid import covid_api # Blueprint import api definition

from bp_projects.projects import app_projects # Blueprint directory import projects definition
from model_users import model_builder

app.register_blueprint(app_api) # register api routes
#app.register_blueprint(covid_api) # register api routes

app.register_blueprint(app_projects) # register api routes

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.route('/purpose/')  # connects /stub/ URL to stub() function
def purpose():
    return render_template("purpose.html")

@app.before_first_request
def activate_job():
    model_builder()
    
# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volumes/sqlite.db'
    app.run(debug=True, host="0.0.0.0", port="8086")