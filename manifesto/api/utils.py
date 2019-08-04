from datetime import datetime

from manifesto.database.models import db
from manifesto.database.models.manifesto import Manifesto
from manifesto.database.models.proposal import Proposal


schemas = {
    '1.0': {
        'manifesto': {
            'political_party': 'politicalParty',
            'title': 'title',
            'publication_date': 'publication_date',
            'election_date': 'election_date',
            'type_of_elections': 'type_of_elections',
            'geographical_area': 'geographical_area',
            'version': 'version',
            'uri': 'uri',
            'created_by': 'created_by',
            'pages': 'pages',
            'num_proposals': 'num_proposals',
        },
        'proposal': {
            'id_proposal': 'id',
            'body': 'body',
            'topic': 'topic',
            'tags': 'tags',
            'priority': 'priority',
            'budget': 'budget',
            'non_negotiable': 'non-negotiable',
            'agents': 'agents',
        }
    },
    '1.1': {
        'manifesto': {
            'political_party': 'politicalParty',
            'title': 'title',
            'publication_date': 'publicationDate',
            'election_date': 'electionDate',
            'type_of_elections': 'electionsType',
            'geographical_area': 'geographicalArea',
            'version': 'standardVersion',
            'uri': 'URI',
            'created_by': 'createdBy',
            'pages': 'pages',
            'num_proposals': 'numProposals',
        },
        'proposal': {
            'id_proposal': 'id',
            'body': 'body',
            'topic': 'topic',
            'tags': 'tags',
            'priority': 'priority',
            'budget': 'budget',
            'non_negotiable': 'nonNegotiable',
            'agents': 'agents',
        }

    }
}

def json2db(data):
    """ Transform json in instance object. Save Manifesto and proposal in
    database. """
    proposals_data = data.pop('proposals', [])
    version = data.get('version')
    schema = schemas.get(version)

    manifesto = Manifesto()
    for k, v in schema.get('manifesto').items():
        value = data.pop(v, None)
        if value:
            # Fix date format: force date format YYYY-MM-DD, then rm this code
            if k in ['publication_date', 'election_date']:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        value = datetime.strptime(value, '%d/%m/%Y').date()
                    except ValueError:
                        value = None
            # end fix
            setattr(manifesto, k, value)
    db.session.add(manifesto)
    db.session.commit()

    for proposal_data in proposals_data:
        proposal = Proposal()
        for k, v in schema.get('proposal').items():
            value = proposal_data.pop(v, None)
            if value is not None:
                if k in ['budget', 'non_negotiable'] and not isinstance(value, bool):
                    continue
                setattr(proposal, k, value)
        proposal.id_manifesto = manifesto.id
        db.session.add(proposal)
    db.session.commit()
