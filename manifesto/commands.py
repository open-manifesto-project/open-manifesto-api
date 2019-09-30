import click
import json
import os

from flask.cli import AppGroup

from manifesto.api.utils import json2db


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
