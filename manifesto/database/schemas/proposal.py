from flask_restplus import fields


simple_serializer = {
    'id': fields.Integer
}

serializer = {
    'id': fields.Integer(required=True, description='The manifesto identifier'),
    'id_proposal': fields.Integer(description=''),
    'body': fields.String(description=''),
    'topics': fields.List(fields.String(description='')),
    'tags': fields.List(fields.String(description='')),
    'priority': fields.String(description=''),
    'budget': fields.Boolean(description=''),
    'non_negotiable': fields.Boolean(description=''),
    'agents': fields.List(fields.String(description='')),
    'id_manifesto': fields.Integer(description=''),
}
