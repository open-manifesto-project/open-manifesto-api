import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto


app.config.from_object('manifesto.config.TestingConfig')


class ManifestoTests(unittest.TestCase, FixturesMixin):

    fixtures = ['manifesto.json']
    # Fixture contains:
    # * 1 manifesto with id=100
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
            'election_type',
            'geographical_area',
            'id',
            'num_proposals',
            'pages',
            'political_party',
            'proposals',
            'publication_date',
            'title',
            'uri',
            'version'
        ]
        self.manifesto_keys_2 = self.manifesto_keys.copy()
        self.manifesto_keys_2.remove('proposals')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_manifesto(self):
        response = self.client.get('/manifestos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(sorted(response.get_json()[0].keys()), self.manifesto_keys_2)

    def test_list_manifesto_filter(self):
        political_party = Manifesto.query.first().political_party
        args = 'political_party={}'.format(political_party)
        response = self.client.get('/manifestos?{}'.format(args))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(sorted(response.get_json()[0].keys()), self.manifesto_keys_2)

    def test_list_manifesto_filter_bad_request(self):
        political_party = Manifesto.query.first().political_party + 'x'
        args = 'election_date={}'.format('bad request')
        response = self.client.get('/manifestos?{}'.format(args))
        self.assertEqual(response.status_code, 400)

    def test_get_manifesto(self):
        response = self.client.get('/manifestos/100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(response.get_json().keys()), self.manifesto_keys)
        proposals = response.get_json().get('proposals')
        self.assertTrue(isinstance(proposals, list))
        self.assertTrue('id' in proposals[0].keys())
        self.assertTrue('body' in proposals[0].keys())

    def test_get_election_types(self):
        response = self.client.get('/manifestos/election-types')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_geographical_areas(self):
        response = self.client.get('/manifestos/geographical-areas')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_political_parties(self):
        response = self.client.get('/manifestos/political-parties')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)


if __name__ == '__main__':
    unittest.main()
