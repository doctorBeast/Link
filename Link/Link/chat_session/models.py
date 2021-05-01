import datetime
from mongoengine.fields import StringField, DateTimeField, EmbeddedDocumentListField, ListField, ReferenceField, \
    EmbeddedDocument
from mongoengine import DynamicDocument
from Link.user.models import User
from wtforms.validators import ValidationError


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
    temp = ListField(required=True, field=StringField())
    owner = ReferenceField(User, required=True)
    type = StringField(required=True, choices=['DM', 'GROUP'], default='DM')
    messages = EmbeddedDocumentListField(required=True, document_type=Message)

    allowed_update_fields = []
