from base64 import b64decode
import hmac, hashlib
import json
import requests
import os

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, reqparse

from manifesto.api.utils import json2db


ns = Namespace('hook', description='Hooks')


@ns.route('')
@ns.doc(False)
class HookRegister(Resource):

    def extract_files(self, payload):
        """ Extract new, remove and modify files from payload """
        new_files = []
        rm_files = []
        modify_files = []
        for commit in payload.get('commits', []):
            new_files += commit.get('added', [])
            rm_files += commit.get('removed', [])
            modify_files += commit.get('modified', [])
        return new_files, rm_files, modify_files

    @ns.doc('hook_register')
    def post(self):
        '''Endpoint for receive github webhook'''
        secret_key = current_app.config['SECRET_KEY'].encode()
        signature = request.headers.get('X-Hub-Signature')
        digest = hmac.new(secret_key, request.data, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(signature, "sha1=" + digest):
            return '', 400

        owner = current_app.config['REPO_OWNER']
        repo = current_app.config['REPO_REPO']

        payload = self.api.payload
        commit_after = payload.get('after')
        commit_before = payload.get('before')
        new_files, rm_files, modify_files = self.extract_files(payload)

        url = 'https://api.github.com/repos/{}/{}/contents/{}?ref={}'

        for new_file in new_files:
            req = requests.get(url.format(owner, repo, new_file, commit_after))
            if req.status_code == 200:
                data = json.loads(b64decode(req.json().get('content')))
            else:
                return '', req.status_code
            json2db(data)
        for rm_file in rm_files:
            req = requests.get(url.format(owner, repo, rm_file, commit_before))
            if req.status_code == 200:
                old_data = json.loads(b64decode(req.json().get('content')))
            else:
                return '', req.status_code
            json2db({}, old_data=old_data, mode='rm')
        for modify_file in modify_files:
            req_after = requests.get(url.format(owner, repo, modify_file, commit_after))
            if req_after.status_code == 200:
                data = json.loads(b64decode(req_after.json().get('content')))
            else:
                return '', req_after.status_code
            req_before = requests.get(url.format(owner, repo, modify_file, commit_before))
            if req_before.status_code == 200:
                old_data = json.loads(b64decode(req_before.json().get('content')))
            else:
                return '', req_before.status_code
            json2db(data, old_data=data, mode='modify')

        return '', 200
