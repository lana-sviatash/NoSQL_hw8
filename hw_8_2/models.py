from mongoengine import Document, StringField, BooleanField, connect

uri = "mongodb+srv://goitlearn:EonuZ7uxhFxUO8MQ@cluster0.mcqnxq7.mongodb.net/?retryWrites=true&w=majority"
connect(host=uri)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(max_length=40)
    confirm = BooleanField(default=False)
