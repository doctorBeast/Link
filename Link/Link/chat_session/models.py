import datetime
from mongoengine.fields import StringField, DateTimeField, EmbeddedDocumentListField, ListField, ReferenceField, \
    EmbeddedDocument
from mongoengine import DynamicDocument
from Link.user.models import User
from Link.helper.mongo_to_dict import mongo_to_dict
from bson import json_util
from Link.framework.exception import ValidationError


def check_members_field(data=[]):
    if not isinstance(data, list):
        raise ValidationError("Field Value not List Type")
    if len(data) < 2:
        raise ValidationError("Not enough members provided")
    if len(data) != len(set(data)):
        raise ValidationError("Field values cannot be repeated")


class Message(EmbeddedDocument):
    created_date = DateTimeField(required=True, default=datetime.datetime.now())
    creator = ReferenceField(User)
    data = StringField(required=True)


class ChatSession(DynamicDocument):
    """Needs to have fields like Modified Date field, members, messages"""
    created_date = DateTimeField(required=True, default=datetime.datetime.now())
    modified_date = DateTimeField(required=True, default=datetime.datetime.now())
    members = ListField(required=True, field=ReferenceField(User), validation=check_members_field)
    owner = ReferenceField(User)# Not taking this field seriously since first we need the normal msging to work.
    type = StringField(required=True, choices=['DM', 'GROUP'], default='DM')
    messages = EmbeddedDocumentListField(required=True, document_type=Message)

    allowed_update_fields = []

    def to_dict(self, exclude_fields=[]):
        return mongo_to_dict(self, exclude_fields)

    # https://stackoverflow.com/questions/23977951/how-to-get-referencefield-data-in-mongoengine
    # def to_json_with_members(self):
    #     data = self.to_mongo()
    #     members = []
    #     for member in self.members:
    #         temp = {
    #             "name": member.name,
    #             "_id": member.id
    #         }
    #         members.append(temp)
    #     data["members"] = members
    #     return json_util.dumps(data)


