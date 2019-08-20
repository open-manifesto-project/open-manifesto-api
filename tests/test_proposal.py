import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db


app.config.from_object('manifesto.config.TestingConfig')


class ProposalTests(unittest.TestCase, FixturesMixin):

    fixtures = ['manifesto.json']
    # Fixture contains:
    # * 1 manifesto
    # * 166 proposals
    app = app
    db = db

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()
        self.proposal_keys = [
            'agents',
            'body',
            'budget',
            'id',
            'id_manifesto',
            'id_proposal',
            'non_negotiable',
            'priority',
            'tags',
            'topics'
        ]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_proposals(self):
        response = self.client.get('/api/proposal')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 166)
        self.assertEqual(sorted(response.get_json()[0].keys()), self.proposal_keys)

    def test_get_proposal(self):
        response = self.client.get('/api/proposal/1')
        self.assertEqual(response.status_code, 200)

    def test_get_topics(self):
        response = self.client.get('/api/proposal/topic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_get_priorities(self):
        response = self.client.get('/api/proposal/priority')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))


if __name__ == '__main__':
    unittest.main()
