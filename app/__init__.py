from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.extensions import db
from app.main import main as main_blueprint
from app.auth import auth as auth_blueprint
from config import DevelopmentConfig, ProductionConfig

def create_app():
    app = Flask(__name__)

    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)


    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    db.init_app(app)
    
    @app.cli.command("init-db")
    def init_db():
        """Create database tables from SQLAlchemy models."""
        db.create_all()
        print("Initialized the database.")

    return app

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='5000', debug=True)
