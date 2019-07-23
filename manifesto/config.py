import os


DT_FMT = "%Y-%m-%d %H:%M:%S %z"


class BaseConfig:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # Flask-Restplus settings
    RESTPLUS_VALIDATE = True
    ERROR_404_HELP = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_LANGUAGES = ['en', 'es']

    #SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_ECHO = True

    SECRET_KEY = 'manifesto_pass'


class DevConfig(BaseConfig):
    DEBUG = True


class PostgresConfig(BaseConfig):
    POSTGRES = {
        'user': 'manifesto',
        'pwd': 'manifesto',
        'db': 'manifesto',
        'host': 'db',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{db}'.format(**POSTGRES)


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # Path relatives to project
    FIXTURES_DIRS = ['tests/event/fixtures', 'tests/player/fixtures']

try:  # pragma: no cover
    from manifesto.local_config import *
except ImportError:  # pragma: no cover
    print('No local config found')
    pass
