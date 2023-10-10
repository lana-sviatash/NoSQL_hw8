from mongoengine import Document, StringField, ListField, ReferenceField, connect
from connect import uri

connect(host=uri)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=50)
    description = StringField(max_length=None)    
    
class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author)
    quote = StringField()
