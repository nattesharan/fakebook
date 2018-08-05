from app import db
from mongoengine import Document,StringField
class FakeBookUser(Document):
    email = StringField(max_length=128,required=True)
    password = StringField(max_length=128,required=True)
    first_name = StringField(max_length=20,required=True)
    last_name = StringField(max_length=20,required=True)