from flask_restplus import Namespace, Resource, fields

from manifesto.models import db


ns = Namespace('hook', description='Hooks')


@ns.route('/')
class HookRegister(Resource):

    @ns.doc('hook_register')
    def post(self):
        '''Endpoint for receive github webhook'''
        # TODO
        return '', 200
