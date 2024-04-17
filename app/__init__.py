from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.extensions import db, migrate
from app.main import main as main_blueprint
from app.auth import auth as auth_blueprint
from app.vision.synthesis import ImageSynthesiser
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    print(os.getenv('FLASK_ENV'))
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.secret_key = app.config['FLASK_SECRET_KEY']
    app.config

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    db.init_app(app)
    @app.cli.command("init-db")
    def init_db():
        """Create database tables from SQLAlchemy models."""
        db.create_all()
        print("Initialized the database.")

    migrate.init_app(app, db)
    from app.auth.models import User

    synthesiser = ImageSynthesiser()  # Create an instance of ImageSynthesiser

    @app.before_request
    def preload_synthesiser():
        # Preload the ImageSynthesiser during app startup
        if not hasattr(app, '_got_first_request'):
            synthesiser.preload()
            app._got_first_request = True

    return app

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='5000', debug=True)