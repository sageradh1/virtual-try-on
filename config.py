import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv

#Loading environment from .startingenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

class Config(object):
    UPLOADED_PHOTOS_DEST =  basedir+"/app/static/uploaded"
    GENERATED_PHOTOS_DEST =  basedir+"/app/static/generated"
    CLOTHES_PHOTOS_DEST =  basedir+"/app/static/clothes"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #max allowed video filesize is 16MB
    ALLOWED_PHOTO_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_KEY=os.getenv('API_KEY')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    API_BASE_URL = "http://127.0.0.1:8080"
    FLASK_ENV = os.getenv('FLASK_ENV')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


