from flask_restplus import Namespace, Resource

from manifesto.database.schemas.proposal import serializer as ser_proposal


ns = Namespace('proposals', description='Proposal related operations')
proposal = ns.model('Proposal', ser_proposal)


@ns.route('')
class ProposalList(Resource):
    @ns.doc('list_proposals')
    @ns.marshal_list_with(proposal)
    def get(self):
        '''List all proposals'''
        # TODO
        return []


@ns.route('/<id>')
@ns.response(404, 'Proposal not found')
@ns.param('id', 'The proposal identifier')
class ProposalParam(Resource):
    '''Show a single proposal item'''
    @ns.doc('get_proposal')
    @ns.marshal_with(proposal)
    def get(self, id):
        '''Fetch a proposal given its identifier'''
        # TODO
        return ''
