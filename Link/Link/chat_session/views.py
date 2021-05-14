from flask import request, Response
from flask.views import MethodView
from .models import ChatSession, Message
from .service import get_all_chat_sessions, get_single_chat_session, create_chat_session, update_chat_session, \
    update_chat_session_message
from bson import ObjectId
from flask_security import current_user, auth_token_required
from .serializer import ChatSessionSerializer
from Link.framework.serializer import Serializer


class ChatSessionAPI(MethodView):
    serializer = ChatSessionSerializer(document_cls=ChatSession)

    @auth_token_required
    def get(self, id):
        if not id:
            chat_sessions = get_all_chat_sessions(user_id=current_user.id)
            chat_sessions = self.serializer.serialize(chat_sessions)
            return Response(chat_sessions, mimetype="application/json", status=200)
        else:
            id = ObjectId(id)
            chat_session = get_single_chat_session(eid=id, user_id=current_user.id)
            chat_session = self.serializer.serialize(chat_session)
            return Response(chat_session, mimetype="application/json", status=200)

    @auth_token_required
    def post(self, id):
        # chat session owner field is taking any string value
        chat_session_data = request.get_json()
        result = create_chat_session(chat_session_data)
        return result, 200

    @auth_token_required
    def put(self, id):
        chat_session_data = request.get_json()
        update_chat_session(id, chat_session_data)
        return '', 200


class MessageAPI(MethodView):
    serializer = Serializer(document_cls=Message)

    @auth_token_required
    def get(self, id):
        chat_session_id = id
        messages = ChatSession.objects(id=chat_session_id).fields(slice__messages=[0, 2]).to_json()
        return Response(messages, mimetype="application/json", status=200)

    @auth_token_required
    def post(self, id):
        chat_session_id = id
        message_data = request.get_json()
        message = update_chat_session_message(chat_session_id, message_data)
        message = self.serializer.serialize(message)
        return Response(message, mimetype="application/json", status=200)
