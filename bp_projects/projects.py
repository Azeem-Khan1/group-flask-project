from flask import Blueprint, render_template

app_projects = Blueprint('projects', __name__,
                url_prefix='/projects',
                template_folder='templates/bp_projects/')

# connects /kangaroos path to render kangaroos.html
@app_projects.route('/chinmay/')
def portfolio():
    return render_template("chinmay.html")

# connects /kangaroos path to render kangaroos.html
@app_projects.route('/varalu/')
def kangaroos():
    return render_template("varalu.html")

@app_projects.route('/collin/')
def walruses():
    return render_template("collin.html")

@app_projects.route('/azeem/')
def hawkers():
    return render_template("azeem.html")