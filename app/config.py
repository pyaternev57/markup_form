"""Flask app configuration."""
from os import environ

class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    # SECRET_KEY = 'nl2ml'
    # UPLOAD_FOLDER = 'upload/'
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = {'csv'}

    # Flask-SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db:3306/nl2ml'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')
