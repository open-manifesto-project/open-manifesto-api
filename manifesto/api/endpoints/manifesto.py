from datetime import datetime
from flask import request
from flask_restplus import Namespace, Resource

from manifesto.database.models.manifesto import Manifesto
from manifesto.database.schemas.manifesto import serializer, serializer_with_proposal


ns = Namespace('manifestos', description='Manifesto related operations')
manifesto = ns.model('Manifesto', serializer)
manifesto_with_proposals = ns.model('Manifesto', serializer_with_proposal)

date_type = lambda x: datetime.strptime(x,'%Y-%m-%d').date()

parser = ns.parser()
parser.add_argument('political_party', type=str, help='Political party')
parser.add_argument('election_type', type=str, help='Election type')
parser.add_argument('geographical_area', type=str, help='Geographical area')
parser.add_argument('election_date', type=date_type, help='Election type with format YYYY-M-DD')


@ns.route('')
class ManifestoList(Resource):
    @ns.expect(parser, validate=True)
    @ns.marshal_list_with(manifesto)
    def get(self):
        '''List all manifestos'''
        args = parser.parse_args()
        args_not_none = {k: v for k, v in args.items() if v is not None}
        return Manifesto.query.filter_by(**args_not_none).all()


@ns.route('/<id>')
@ns.response(404, 'Manifesto not found')
@ns.param('id', 'The manifesto identifier')
class ManifestoParam(Resource):
    '''Show a single manifesto item'''
    @ns.doc('get_manifesto')
    @ns.marshal_with(manifesto_with_proposals)
    def get(self, id):
        '''Fetch a manifesto given its identifier'''
        return Manifesto.query.get(id)


@ns.route('/election-types')
class ManifestoElectionType(Resource):
    @ns.doc('election_types')
    def get(self):
        '''List election types'''
        col = Manifesto.election_type
        query = Manifesto.query.with_entities(col).filter(col.isnot(None)).distinct().all()
        return list(*zip(*query))


@ns.route('/geographical-areas')
class ManifestoGeographicalArea(Resource):
    @ns.doc('geographical_areas')
    def get(self):
        '''List geographical areas'''
        col = Manifesto.geographical_area
        query = Manifesto.query.with_entities(col).filter(col.isnot(None)).distinct().all()
        return list(*zip(*query))


@ns.route('/political-parties')
class ManifestoPoliticalParty(Resource):
    @ns.doc('political_parties')
    def get(self):
        '''List political parties'''
        col = Manifesto.political_party
        query = Manifesto.query.with_entities(col).filter(col.isnot(None)).distinct().all()
        return list(*zip(*query))
