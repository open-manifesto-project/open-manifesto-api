from flask_restplus import Namespace, Resource
from sqlalchemy import func

from manifesto.database.models import db
from manifesto.database.models.proposal import Proposal
from manifesto.database.schemas.proposal import serializer as ser_proposal


ns = Namespace('proposals', description='Proposal related operations')
proposal = ns.model('Proposal', ser_proposal)


@ns.route('')
class ProposalList(Resource):
    @ns.doc('list_proposals')
    @ns.marshal_list_with(proposal)
    def get(self):
        '''List all proposals'''
        return Proposal.query.all()


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
