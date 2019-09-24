from os import environ as env

from flask import Blueprint, url_for
from flask_restplus import Api

from manifesto.api.endpoints.manifesto import ns as ns_manifesto
from manifesto.api.endpoints.proposal import ns as ns_proposal
from manifesto.api.endpoints.hook import ns as ns_hook


bp_api = Blueprint('api', __name__, url_prefix='')
bp_api_v1 = Blueprint('api v1', __name__, url_prefix='/v1')

args = {
    'title': "Open Manifesto Project API",
    'description': "This document includes all the methods that the Open Manifesto Project API offers its users.",
    'doc': '/',
}


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        port = env.get('PORT', '5000')
        scheme = 'http' if port in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


api_v1 = MyApi(bp_api_v1, version='1.0', **args)
api = MyApi(bp_api, version='1.0', **args)

for _api in ('api_v1', 'api'):
    eval(_api).add_namespace(ns_manifesto, path='/manifesto')
    eval(_api).add_namespace(ns_proposal, path='/proposal')
    eval(_api).add_namespace(ns_hook, path='/hook')
