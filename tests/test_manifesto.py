import unittest
from flask_fixtures import FixturesMixin

from manifesto.app import app
from manifesto.database.models import db


app.config.from_object('manifesto.config.TestingConfig')


class ManifestoTests(unittest.TestCase, FixturesMixin):

    fixtures = []
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

    def test_get_manifesto(self):
        response = self.client.get('/api/manifesto/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
