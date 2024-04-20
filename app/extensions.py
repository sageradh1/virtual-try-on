from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.vision.synthesis import ImageSynthesiser
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
synthesiser = ImageSynthesiser()
# synthesiser.preload()
def get_synthesiser():
    return synthesiser