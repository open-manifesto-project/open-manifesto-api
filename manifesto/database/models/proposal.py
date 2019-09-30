from sqlalchemy.dialects.postgresql import ARRAY

from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto


class Proposal(db.Model):
    __tablename__ = 'proposal'
    id = db.Column(db.Integer, primary_key=True)
    proposal_number = db.Column(db.Integer())
    body = db.Column(db.Text())
    topics = db.Column(ARRAY(db.String))
    tags = db.Column(ARRAY(db.String))
    priority = db.Column(db.String(16))
    budget = db.Column(db.Boolean())
    non_negotiable = db.Column(db.Boolean())
    agents = db.Column(ARRAY(db.String))
    id_manifesto = db.Column(db.Integer(), db.ForeignKey(Manifesto.id, ondelete='CASCADE'))
