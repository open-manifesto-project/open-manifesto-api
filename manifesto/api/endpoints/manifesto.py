from flask_restplus import Namespace, Resource

from manifesto.database.schemas.manifesto import serializer as ser_manifesto


ns = Namespace('manifestos', description='Manifesto related operations')
manifesto = ns.model('Manifesto', ser_manifesto)


@ns.route('')
class ManifestoList(Resource):
    @ns.doc('list_manifestos')
    @ns.marshal_list_with(manifesto)
    def get(self):
        '''List all manifestos'''
        # TODO
        return []


@ns.route('/<id>')
@ns.response(404, 'Manifesto not found')
@ns.param('id', 'The manifesto identifier')
class ManifestoParam(Resource):
    '''Show a single manifesto item'''
    @ns.doc('get_manifesto')
    @ns.marshal_with(manifesto)
    def get(self, id):
        '''Fetch a manifesto given its identifier'''
        # TODO
        return ''
