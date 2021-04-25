from flask import request, Response
from flask.views import MethodView
from .models import ChatSession, Message
from .service import create_chat_session, update_chat_session, update_chat_session_message
from bson import ObjectId
from Link.user.models import User


class ChatSessionAPI(MethodView):

    def get(self, id):
        if not id:
            chat_sessions = ChatSession.objects().to_json()
            return Response(chat_sessions, mimetype="application/json", status=200)
        else:
            id = ObjectId(id)
            chat_session = ChatSession.objects().get(id=id).to_json()
            return Response(chat_session, mimetype="application/json", status=200)

    def post(self, id):
        # chat session owner field is taking any string value
        chat_session_data = request.get_json()
        result = create_chat_session(chat_session_data)
        return result, 200

    def put(self, id):
        chat_session_data = request.get_json()
        update_chat_session(id, chat_session_data)
        return '', 200


class MessageAPI(MethodView):

    def get(self, id):
        chat_session_id = id
        messages = ChatSession.objects(id=chat_session_id).fields(slice__messages=[0, 2]).to_json()
        return Response(messages, mimetype="application/json", status=200)

    def post(self, id):
        chat_session_id = id
        message_data = request.get_json()
        update_chat_session_message(chat_session_id, message_data)
        return '', 200
