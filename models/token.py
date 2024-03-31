from mongoengine import Document, StringField


class Token(Document):
    tokenValue = StringField(required=True)
    userId = StringField(required=True)
