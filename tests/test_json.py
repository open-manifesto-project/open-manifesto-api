import json
import os
import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto
from manifesto.database.models.proposal import Proposal
from manifesto.api.utils import json2db


app.config.from_object('manifesto.config.TestingConfig')


class JsonTests(unittest.TestCase):

    app = app
    db = db

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_load_json_in_db(self):
        """ Load severals json and save in database """
        amount_manifestos = Manifesto.query.count()
        amount_proposals = Proposal.query.count()
        base_dir = 'tests/schemas/'
        for filename in os.listdir(base_dir):
            with open(os.path.join(base_dir, filename), 'r') as f:
                data = json.load(f)
                amount_proposals += int(data.get('num_proposals', 0))
                amount_manifestos += 1
                json2db(data)
        self.assertEqual(Manifesto.query.count(), amount_manifestos)
        self.assertEqual(Proposal.query.count(), amount_proposals)

if __name__ == '__main__':
    unittest.main()
