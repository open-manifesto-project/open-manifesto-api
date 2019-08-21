import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto


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
        self.manifesto_keys = [
            'created_by',
            'election_date',
            'geographical_area',
            'id',
            'num_proposals',
            'pages',
            'political_party',
            'proposals',
            'publication_date',
            'title',
            'type_of_elections',
            'uri',
            'version'
        ]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_manifesto(self):
        response = self.client.get('/api/manifesto')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(sorted(response.get_json()[0].keys()), self.manifesto_keys)

    def test_list_manifesto_filter(self):
        political_party = Manifesto.query.first().political_party
        args = 'political_party={}'.format(political_party)
        response = self.client.get('/api/manifesto?{}'.format(args))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(sorted(response.get_json()[0].keys()), self.manifesto_keys)

    def test_list_manifesto_filter_bad_request(self):
        political_party = Manifesto.query.first().political_party + 'x'
        args = 'election_date={}'.format('bad request')
        response = self.client.get('/api/manifesto?{}'.format(args))
        self.assertEqual(response.status_code, 400)

    def test_get_manifesto(self):
        response = self.client.get('/api/manifesto/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(response.get_json().keys()), self.manifesto_keys)

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
