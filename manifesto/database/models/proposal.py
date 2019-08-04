from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto


class Proposal(db.Model):
    __tablename__ = 'proposal'
    id = db.Column(db.Integer, primary_key=True)
    id_proposal = db.Column(db.Integer())
    body = db.Column(db.Text())
    topic = db.Column(db.String(256))
    tags = db.Column(db.ARRAY(db.String))
    priority = db.Column(db.String(16))
    budget = db.Column(db.Boolean())
    non_negotiable = db.Column(db.Boolean())
    agents = db.Column(db.ARRAY(db.String))
    id_manifesto = db.Column(db.Integer(), db.ForeignKey(Manifesto.id))
