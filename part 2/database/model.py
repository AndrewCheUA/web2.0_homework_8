from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, BooleanField


class Contacts(Document):
    fullname = StringField()
    phone = StringField()
    email = StringField()
    email_preferred = BooleanField()
    message_sent = BooleanField()