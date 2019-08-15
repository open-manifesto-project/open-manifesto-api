import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db


app.config.from_object('manifesto.config.TestingConfig')


class ManifestoTests(unittest.TestCase, FixturesMixin):

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_manifesto(self):
        response = self.client.get('/api/manifesto')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        keys = sorted(['id'])
        self.assertEqual(sorted(response.get_json()[0].keys()), keys)

    def test_get_manifesto(self):
        response = self.client.get('/api/manifesto/1')
        self.assertEqual(response.status_code, 200)
        keys = sorted(['id'])
        self.assertEqual(sorted(response.get_json().keys()), keys)

    def test_get_election_types(self):
        response = self.client.get('/api/manifesto/election-type')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_geographical_areas(self):
        response = self.client.get('/api/manifesto/geographical-area')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_political_parties(self):
        response = self.client.get('/api/manifesto/political-party')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)


if __name__ == '__main__':
    unittest.main()
