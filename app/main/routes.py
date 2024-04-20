from flask import jsonify, render_template, request
from . import main
from app.logger import app_logger

@main.route('/health-check', methods=['GET'])
def index():
    app_logger.info("Health-check")
    return jsonify({
        "status": 200,
        "message": "success"
    })

@main.route('/', methods=['GET'])
def main_index():
    # app_logger.info("Health-check")
    if request.method == 'GET':
            return render_template('main/index.html')