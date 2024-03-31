from mongoengine import Document, StringField, FloatField


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    mailboxSize = FloatField(required=True)
    mailboxUnit = StringField(required=True)
