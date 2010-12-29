from settings import DB


_document_names = set(['issue'])

_sequences_names = DB['sequences'].distinct('_id')

for _sequence_name in _document_names.difference(_sequences_names):
    DB['sequences'].insert({'_id': _sequence_name, 'pk': 0})

def get_next_pk(sequence_name):
    return DB.command('findAndModify', 'sequences',
        query={'_id': sequence_name}, update={'$inc': {'pk': 1}},
        new=True)['value']['pk']
