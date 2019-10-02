from flask_restplus import Namespace, Resource
from sqlalchemy import and_, cast, func
from sqlalchemy.dialects.postgresql import ARRAY

from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto
from manifesto.database.models.proposal import Proposal
from manifesto.database.schemas.proposal import serializer, simple_serializer
from manifesto.api.utils import bloom_intersection


ns = Namespace('proposals', description='Proposal related operations')
proposal = ns.model('Proposal', serializer)
simple_proposal = ns.model('Proposal', simple_serializer)

date_type = lambda x: datetime.strptime(x,'%Y-%m-%d').date()

parser = ns.parser()
parser.add_argument('political_party', type=str, help='Political party')
parser.add_argument('election_type', type=str, help='Election type')
parser.add_argument('geographical_area', type=str, help='Geographical area')
parser.add_argument('election_date', type=date_type, help='Election type with format YYYY-M-DD')
parser.add_argument('topics', type=str, help='Topics: search if the topics exist')
parser.add_argument('tags', type=str, help='Tags (comma separated values)')
parser.add_argument('priority', type=str, help='Priority')
parser.add_argument('budget', type=bool, help='Budget')
parser.add_argument('non_negotiable', type=bool, help='Non negotiable')
parser.add_argument('agents', type=str, help='Agents: search if the agents exist')
parser.add_argument('threshold', type=float, help='Tag threshold overlap: Float number between 0 and 1. 0 one tag exist and 1 every tag exists')


@ns.route('')
class ProposalList(Resource):

    def filter_proposal(self, proposals, tags, threshold):
        ''' Filter proposal depend on threshold tags. '''
        filter_proposals = []
        for proposal in proposals:
            overlap = len(set(proposal.tags) & set(tags))
            if overlap / len(tags) >= threshold:
                filter_proposals.append(proposal)
        return filter_proposals

    @ns.doc('list_proposals')
    @ns.expect(parser, validate=True)
    @ns.marshal_list_with(simple_proposal)
    def get(self):
        '''List all proposals'''
        arg_manifesto = [
            'political_party',
            'election_type',
            'geographical_area',
            'election_date'
        ]
        tags = []
        threshold = 0
        args = parser.parse_args()
        args_manifesto = {}
        args_filter_manifesto = []
        args_proposal = {}
        for k, v in args.items():
            if v is None:
                continue
            if k in arg_manifesto:
                args_manifesto[k] = v
            elif k in ['agents', 'topics']:
                args_filter_manifesto.append(getattr(Proposal, k).any(v))
            elif k == 'tags':
                tags = v.split(',')
                v_cast = cast(tags, ARRAY(db.String))
                args_filter_manifesto.append(getattr(Proposal, k).overlap(v_cast))
            elif k == 'threshold':
                if 'tags' in args:
                    threshold = float(v)
            else:
                args_proposal[k] = v
        result = Proposal.query.filter_by(**args_proposal)\
                .filter(and_(*args_filter_manifesto)).join(Manifesto)\
                .filter(Manifesto.id == Proposal.id_manifesto)\
                .filter_by(**args_manifesto).all()
        return self.filter_proposal(result, tags, threshold) if threshold else result


@ns.route('/<id>')
@ns.response(404, 'Proposal not found')
@ns.param('id', 'The proposal identifier')
class ProposalParam(Resource):
    '''Show a single proposal item'''
    @ns.doc('get_proposal')
    @ns.marshal_with(proposal)
    def get(self, id):
        '''Fetch a proposal given its identifier'''
        return Proposal.query.get(id)


@ns.route('/topics')
class ProposalTopic(Resource):
    @ns.doc('proposal_topics')
    def get(self):
        '''List proposal topics'''
        query = db.session.query(func.unnest(Proposal.topics)).distinct().all()
        return list(*zip(*query))


@ns.route('/priorities')
class ProposalPriority(Resource):
    @ns.doc('proposal_priorities')
    def get(self):
        '''List proposal priorities'''
        col = Proposal.priority
        query = Proposal.query.with_entities(col).filter(col.isnot(None)).distinct().all()
        return list(*zip(*query))
