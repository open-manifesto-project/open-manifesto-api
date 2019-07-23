import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db
from tests.base import ClientJSON


app.config.from_object('manifesto.config.TestingConfig')


class ManifestoTests(unittest.TestCase, FixturesMixin):

    fixtures = []
    app = app
    db = db

    def setUp(self):
        self.client = ClientJSON(app)

    def test_list_manifesto(self):
        response = self.client.get('/api/manifesto')
        self.assertEqual(response.status_code, 200)

    def test_get_manifesto(self):
        response = self.client.get('/api/manifesto/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
