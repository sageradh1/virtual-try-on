from flask import jsonify, render_template
from . import main
from app.logger import app_logger

@main.route('/health-check', methods=['GET'])
def index():
    app_logger.info("Health-check")
    return jsonify({
        "status": 200,
        "message": "success"
    })
