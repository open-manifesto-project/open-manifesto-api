from flask_restplus import Namespace, Resource
from sqlalchemy import and_, func

from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto
from manifesto.database.models.proposal import Proposal
from manifesto.database.schemas.proposal import serializer as ser_proposal
from manifesto.api.utils import bloom_intersection


ns = Namespace('proposals', description='Proposal related operations')
proposal = ns.model('Proposal', ser_proposal)

date_type = lambda x: datetime.strptime(x,'%Y-%m-%d').date()

parser = ns.parser()
parser.add_argument('political_party', type=str, help='Political party')
parser.add_argument('type_of_elections', type=str, help='Election type')
parser.add_argument('geographical_area', type=str, help='Election type')
parser.add_argument('election_date', type=date_type, help='Election type with format YYYY-M-DD')
parser.add_argument('topics', type=str, help='Topics: search if the topics exist')
parser.add_argument('tags', type=str, help='Tags: search if the tags exist')
parser.add_argument('priority', type=str, help='Priority')
parser.add_argument('budget', type=bool, help='Budget')
parser.add_argument('non_negotiable', type=bool, help='Non negotiable')
parser.add_argument('agents', type=str, help='Agents: search if the agents exist')


@ns.route('')
class ProposalList(Resource):
    @ns.doc('list_proposals')
    @ns.expect(parser, validate=True)
    @ns.marshal_list_with(proposal)
    def get(self):
        '''List all proposals'''
        arg_manifesto = [
            'political_party',
            'type_of_elections',
            'geographical_area',
            'election_date'
        ]
        tags = None
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
            else:
                args_proposal_by[k] = v
        proposals = Proposal.query.filter_by(**args_proposal)\
                .filter(and_(*args_filter_manifesto)).join(Manifesto)\
                .filter(Manifesto.id == Proposal.id_manifesto)\
                .filter_by(**args_manifesto).all()
        if tags:
            proposals_with_tag = []
            for proposal in proposals[:]:
                if bloom_intersection(tags, proposal.tags):
                    proposals_with_tag.append(proposal)
            return proposals_with_tag
        else:
            return proposals


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


@ns.route('/topic')
class ProposalTopic(Resource):
    @ns.doc('proposal_topics')
    def get(self):
        '''List proposal topics'''
        query = db.session.query(func.unnest(Proposal.topics)).distinct().all()
        return list(zip(*query))


@ns.route('/priority')
class ProposalPriority(Resource):
    @ns.doc('proposal_priorities')
    def get(self):
        '''List proposal priorities'''
        col = Proposal.priority
        query = Proposal.query.with_entities(col).distinct().all()
        return list(zip(*query))
