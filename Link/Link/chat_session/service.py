from .models import ChatSession, Message
from mongoengine.queryset.visitor import Q
from wtforms.validators import ValidationError
import datetime


def create_chat_session(data):
    """

    :param data:
    :return:
    """
    # make all validations on data and then create
    # check if the members pair is unique in collection

    chat_session = ChatSession(**data)
    chat_session.validate()
    members = chat_session.members
    # validate_creators_of_messages
    for msg in chat_session.messages:
        if msg.creator not in members:
            raise ValidationError("Unauthorized Access")
    resp = ChatSession.objects.filter(Q(members__all=members) and Q(type='DM')).count()
    if resp:
        raise ValidationError('Chat Session between Users already exists')
    try:
        chat_session.save()
    except Exception as e:
        raise e
    return {'id': str(chat_session.id)}


def validate_update_chat_session_request(data):
    update_allowed_list = ChatSession.allowed_update_fields
    updated_fields = data.keys()
    check = all(field in update_allowed_list for field in updated_fields)
    if not check:
        raise ValidationError("Update on following fields not allowed")


def update_chat_session(eid, data):
    validate_update_chat_session_request(data)
    data["modified_data"] = datetime.datetime.now()
    try:
        ChatSession.objects(id=eid).update(**data)
    except Exception as e:
        raise e
    return True


def update_chat_session_message(eid, data):
    message = Message(**data)
    resp = ChatSession.objects.filter(id=eid, members=data.get('creator'))(id=eid).update(push__messages__0=message, modified_date=datetime.datetime.now())
    if not resp:
        raise ValidationError("Invalid Request")
    return True
