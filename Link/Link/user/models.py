# USERS = [{
#     'name': 'Maggi',
#     'steps': 'XYZ'
# }]

from Link import db
import datetime
from Link.helper.mongo_to_dict import mongo_to_dict
from flask_mongoengine import DynamicDocument

# from Link.framework.models import NubDocument, DynamicNubDocument


class User(db.DynamicDocument):
    created_date = db.DateTimeField(required=True, default=datetime.datetime.now())
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.StringField(required=True)
    status = db.StringField(required=True, choices=['ACTIVE', 'INACTIVE'], default='ACTIVE')

    def to_dict(self, exclude_fields=[]):
        return mongo_to_dict(self, exclude_fields)
