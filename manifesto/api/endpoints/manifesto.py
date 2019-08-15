from flask_restplus import Namespace, Resource

from manifesto.database.models.manifesto import Manifesto
from manifesto.database.schemas.manifesto import serializer as ser_manifesto


ns = Namespace('manifestos', description='Manifesto related operations')
manifesto = ns.model('Manifesto', ser_manifesto)


@ns.route('')
class ManifestoList(Resource):
    @ns.doc('list_manifestos')
    @ns.marshal_list_with(manifesto)
    def get(self):
        '''List all manifestos'''
        return Manifesto.query.all()


@ns.route('/<id>')
@ns.response(404, 'Manifesto not found')
@ns.param('id', 'The manifesto identifier')
class ManifestoParam(Resource):
    '''Show a single manifesto item'''
    @ns.doc('get_manifesto')
    @ns.marshal_with(manifesto)
    def get(self, id):
        '''Fetch a manifesto given its identifier'''
        return Manifesto.query.get(id)


@ns.route('/election-type')
class ManifestoElectionType(Resource):
    @ns.doc('election_types')
    def get(self):
        '''List election types'''
        col = Manifesto.type_of_elections
        query = Manifesto.query.with_entities(col).distinct().all()
        return list(zip(*query))


@ns.route('/geographical-area')
class ManifestoGeographicalArea(Resource):
    @ns.doc('geographical_areas')
    def get(self):
        '''List geographical areas'''
        col = Manifesto.geographical_area
        query = Manifesto.query.with_entities(col).distinct().all()
        return list(zip(*query))


@ns.route('/political-party')
class ManifestoPoliticalParty(Resource):
    @ns.doc('political_parties')
    def get(self):
        '''List political parties'''
        col = Manifesto.political_party
        query = Manifesto.query.with_entities(col).distinct().all()
        return list(zip(*query))
