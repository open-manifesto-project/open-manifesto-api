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
        db.create_all()

    def test_hook(self):
        """ Test hook work """
        filename = 'tests/hook_request/hook.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=9d7413403385409199c69b6a742759e0eb4c3082"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_hook_commit_add_file(self):
        """ Test hook: add new file from a commit """
        new_manifestos = 1
        new_proposals = 166
        amount_manifestos = Manifesto.query.count()
        amount_proposals = Proposal.query.count()
        filename = 'tests/hook_request/hook_add.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=73683fc4af20f28fe633b45bd14527b80ad36961"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manifesto.query.count(), amount_manifestos + new_manifestos)
        self.assertEqual(Proposal.query.count(), amount_proposals + new_proposals)

    def test_hook_commit_rm_file(self):
        """ Test hook: remove file from a commit """
        rm_manifestos = 1
        rm_proposals = 165
        amount_manifestos = Manifesto.query.count()
        amount_proposals = Proposal.query.count()
        filename = 'tests/hook_request/hook_rm.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=6169b147087f52d3868b785e29b5451578a17db1"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manifesto.query.count(), amount_manifestos - rm_manifestos)
        self.assertEqual(Proposal.query.count(), amount_proposals - rm_proposals)

    def test_hook_commit_modify_file(self):
        """ Test hook: modify file from a commit """
        diff_manifestos = 0
        diff_proposals = -1
        amount_manifestos = Manifesto.query.count()
        amount_proposals = Proposal.query.count()
        filename = 'tests/hook_request/hook_modify.json'
        with open(filename, 'r') as f:
            data = json.load(f)
        headers = {"X-Hub-Signature": "sha1=bda3196f4943593f82fe5448dfc32dcfe4f47d1e"}
        response = self.client.post('/api/hook', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Manifesto.query.count(), amount_manifestos + diff_manifestos)
        self.assertEqual(Proposal.query.count(), amount_proposals + diff_proposals)

if __name__ == '__main__':
    unittest.main()
