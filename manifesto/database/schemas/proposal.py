from flask_restplus import fields


serializer = {
    'id': fields.Integer(required=True, description='The manifesto identifier'),
}
