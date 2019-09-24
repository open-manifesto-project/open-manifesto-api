from flask_restplus import Namespace, fields

from manifesto.database.schemas.proposal import serializer


ns = Namespace('proposals', description='Proposal related operations')
proposal = ns.model('Proposal', serializer)


serializer =  {
    'id': fields.Integer(required=True, description='The proposal identifier'),
    'political_party': fields.String(description=''),
    'title': fields.String(description=''),
    'publication_date': fields.Date(dt_format='rfc822', description=''),
    'election_date': fields.Date(dt_format='rfc822', description=''),
    'type_of_elections': fields.String(description=''),
    'geographical_area': fields.String(description=''),
    'version': fields.String(description='', enum=['1.0', '1.1']),
    'uri': fields.String(description=''),
    'created_by': fields.String(description=''),
    'pages': fields.Integer(description=''),
    'num_proposals': fields.Integer(description=''),
}

serializer_with_proposal = serializer.copy()
serializer_with_proposal['proposals'] = fields.List(fields.Nested(proposal))
