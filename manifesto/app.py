#!/usr/bin/env python
from flask import Flask
from flask_cors import CORS

from manifesto.api import bp_api, bp_api_v1
from manifesto.commands import db_cli
from manifesto.config import DevConfig
from manifesto.database.models import db, migrate


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    # SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)


def register_blueprints(app):
    app.register_blueprint(bp_api_v1)
    app.register_blueprint(bp_api)


def register_commands(app):
    app.cli.add_command(db_cli)
