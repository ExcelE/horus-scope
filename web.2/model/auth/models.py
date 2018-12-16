from .common import *
from flask_mongoengine.wtf import model_form
import datetime

class User(Document):
    username = StringField(required=True)
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=30)
    created = DateTimeField(default=datetime.datetime.now)

class Predictions(Document):
    user = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    image = BinaryField()
    created = DateTimeField(default=datetime.datetime.now)
    predict_list = ListField(EmbeddedDocumentField(Guess))

class Guess(EmbeddedDocument):
    description = StringField()
    summary = StringField()
    score = DecimalField()
    url = URLField()