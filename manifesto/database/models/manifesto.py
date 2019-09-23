from manifesto.database.models import db


class Manifesto(db.Model):
    __tablename__ = 'manifesto'
    id = db.Column(db.Integer, primary_key=True)
    political_party = db.Column(db.String(64))
    title = db.Column(db.String(512))
    publication_date = db.Column(db.Date())
    election_date = db.Column(db.Date())
    type_of_elections = db.Column(db.String(64))
    geographical_area = db.Column(db.String(64))
    version = db.Column(db.String(8))
    uri = db.Column(db.String(256))
    created_by = db.Column(db.String(64))
    pages = db.Column(db.Integer())
    num_proposals = db.Column(db.Integer())
    proposals = db.relationship('Proposal', backref='manifesto', passive_deletes=True)
