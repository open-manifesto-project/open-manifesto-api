import os


class BaseConfig:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True

    IP = os.environ.get('IP', '0.0.0.0')
    PORT = os.environ.get('PORT', 4000)

    # Flask-Restplus settings
    RESTPLUS_VALIDATE = True
    ERROR_404_HELP = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_LANGUAGES = ['en', 'es']

    #SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTGRES = {
        'user': 'manifesto',
        'pwd': 'manifesto',
        'db': 'manifesto',
        'host': 'db',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{db}'.format(**POSTGRES)

    SECRET_KEY = 'manifesto_pass'

    REPO_OWNER = 'Virako'
    REPO_REPO = 'Open-Manifesto'


class ProConfig(BaseConfig):
    DEBUG = False


class DevConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    #SQLALCHEMY_ECHO = True
    TESTING = True
    POSTGRES = {
        'user': 'manifesto',
        'pwd': 'manifesto',
        'db': 'test_manifesto',
        'host': 'db-test',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{db}'.format(**POSTGRES)
    FIXTURES_DIRS = ['../tests/fixtures']


try:  # pragma: no cover
    from manifesto.local_config import *
except ImportError:  # pragma: no cover
    print('No local config found')
    pass
