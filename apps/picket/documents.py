from ming import Session, Field, Document, schema
from ming.datastore import DataStore


bind = DataStore('mongodb://localhost:27017/picket')
session = Session(bind)


class Bug(Document):

    class __mongometa__:
        session = session
        name = 'wiki_page'

    _id = Field(schema.ObjectId)
    project = Field(schema.Int)
    reporter = Field(schema.String)
    handler = Field(schema.String)
    priority = Field(schema.OneOf('high', 'normal', 'low'))
    status = Field(schema.OneOf('new', 'assigned', 'resolved'))
    category = Field(schema.String)
    date_submitted = Field(schema.DateTime)
    last_updated = Field(schema.DateTime)
    summary = Field(schema.String)
    description = Field(schema.String)
    attachments = Field(schema.Array(schema.Binary))
