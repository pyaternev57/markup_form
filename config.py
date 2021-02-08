"""Flask app configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    # SECRET_KEY = environ.get('SECRET_KEY')
    SECRET_KEY = 'nl2ml'

    # Flask-SQLAlchemy
    # CREATE USER 'pyaternev'@'%' IDENTIFIED BY 'testpass';
    # CREATE USER 'pyaternev'@'localhost' IDENTIFIED BY 'testpass';
    # grant all  on test.* to pyaternev@localhost
    SQLALCHEMY_DATABASE_URI = 'mysql://pyaternev:testpass@localhost/nl2ml'
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
    # MYSQL_USER = 'flask'
    # MYSQL_PASSWORD = 'password'
    # MYSQL_DB = 'nl2ml'
    # MYSQL_HOST = 'localhost'
