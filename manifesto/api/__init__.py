from flask import Blueprint
from flask_restplus import Api

from manifesto.api.endpoints.manifesto import ns as ns_manifesto
from manifesto.api.endpoints.proposal import ns as ns_proposal
from manifesto.api.endpoints.hook import ns as ns_hook


bp_api = Blueprint('api', __name__, url_prefix='/api')
bp_api_v1 = Blueprint('api v1', __name__, url_prefix='/api/v1')

args = {
    'title': "API project",
    'description': "API versions: <a href='/api/v1/docs'>V1</a> <a href='/api/docs'>latest</a></p>",
    'doc': '/docs',
}

api_v1 = Api(bp_api_v1, version='1.0', **args)
api = Api(bp_api, version='1.0', **args)

for _api in ('api', 'api_v1'):
    eval(_api).add_namespace(ns_manifesto, path='/manifesto')
    eval(_api).add_namespace(ns_proposal, path='/proposal')
    eval(_api).add_namespace(ns_hook, path='/hook')