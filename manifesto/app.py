#!/usr/bin/env python
import click
import json
import os

from flask import Flask
from flask.cli import AppGroup
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from manifesto.api import bp_api, bp_api_v1
from manifesto.api.utils import json2db
from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto
from manifesto.database.models.proposal import Proposal


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object('manifesto.config.DevConfig')

# SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

# Blueprints
app.register_blueprint(bp_api_v1)
app.register_blueprint(bp_api)

# add comand
db_cli = AppGroup('database')

@db_cli.command('initial')
@click.argument('folder')
def initial(folder):
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f:
            print('Reading {} ...'.format(filename))
            data = json.load(f)
            json2db(data, data, mode='modify')
            print('Added {}'.format(filename))

app.cli.add_command(db_cli)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
