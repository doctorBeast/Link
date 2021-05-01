# USERS = [{
#     'name': 'Maggi',
#     'steps': 'XYZ'
# }]

import datetime
from Link.helper.mongo_to_dict import mongo_to_dict
from flask_security import UserMixin, RoleMixin
from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, BooleanField, ReferenceField, ListField
from flask_mongoengine import DynamicDocument


# from Link.framework.models import NubDocument, DynamicNubDocument

class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class User(DynamicDocument, UserMixin):
    created_date = DateTimeField(required=True, default=datetime.datetime.now())
    name = StringField(max_length=50)
    email = StringField(max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])

    def to_dict(self, exclude_fields=[]):
        return mongo_to_dict(self, exclude_fields)
