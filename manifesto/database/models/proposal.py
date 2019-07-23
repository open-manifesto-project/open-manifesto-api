from manifesto.database.models import db


class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100))
    #desc = db.Column(db.String(2048))
    #game = db.Column(db.String(64))
    #platform = db.Column(db.String(64))
    #i18n = db.Column(db.String(32))
    #start_dt = db.Column(db.DateTime())
    #end_dt = db.Column(db.DateTime())
    #players = db.relationship('Player', backref='players', lazy='dynamic')
