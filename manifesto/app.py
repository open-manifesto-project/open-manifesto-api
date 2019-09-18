#!/usr/bin/env python

from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from manifesto.api import bp_api, bp_api_v1
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

with app.app_context():
    db.create_all()
