from flask import Flask
from flask_cors import CORS
import os
from config import DevelopmentConfig, ProductionConfig
from app.extensions import db, migrate
from app.main import main as main_blueprint
from app.auth import auth as auth_blueprint

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    CORS(app, origins="*")

    app.secret_key = os.getenv('FLASK_SECRET_KEY')
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

    migrate.init_app(app, db)
    from app.auth.models import User,GeneratedImage

    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    return app
