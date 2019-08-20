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


class HookTests(unittest.TestCase, FixturesMixin):

    fixtures = ['manifesto.json']
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

    def test_hook_commit_add_file(self):
        """ Test hook: add new file from a commit """
        # initial data
        self.assertEqual(Manifesto.query.count(), 1)
        self.assertEqual(Proposal.query.count(), 166)
        amount_manifestos = Manifesto.query.count()
        amount_proposals = Proposal.query.count()
        filename = 'tests/hook_requests/hook_add.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=73683fc4af20f28fe633b45bd14527b80ad36961"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        # end data
        self.assertEqual(Manifesto.query.count(), 2)
        self.assertEqual(Proposal.query.count(), 166 + 166)

    def test_hook_commit_rm_file(self):
        """ Test hook: remove file from a commit """
        # initial data
        self.assertEqual(Manifesto.query.count(), 1)
        self.assertEqual(Proposal.query.count(), 166)
        filename = 'tests/hook_requests/hook_rm.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=6169b147087f52d3868b785e29b5451578a17db1"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        # end data
        self.assertEqual(Manifesto.query.count(), 0)
        self.assertEqual(Proposal.query.count(), 0)

    def test_hook_commit_modify_file(self):
        """ Test hook: modify file from a commit """
        # initial data
        self.assertEqual(Manifesto.query.count(), 1)
        self.assertEqual(Proposal.query.count(), 166)
        filename = 'tests/hook_requests/hook_modify.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=bda3196f4943593f82fe5448dfc32dcfe4f47d1e"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        # end data
        self.assertEqual(Manifesto.query.count(), 1)
        self.assertEqual(Proposal.query.count(), 165)

if __name__ == '__main__':
    unittest.main()
