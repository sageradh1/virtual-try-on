from flask import Blueprint, render_template

module_one = Blueprint("module_one", __name__, template_folder="templates")

@module_one.route("/")
def index():
    return render_template("index.html")

@module_one.route('/test-route')
def classifier():
    return {
        'code': 200,
        'message': f'Successful',
    }