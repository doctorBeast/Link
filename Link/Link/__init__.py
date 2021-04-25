from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'db': 'linkdb',
                                  'host': 'localhost',
                                  'port': 27017
                                  }
app.debug = True
db = MongoEngine(app)

# from Link.user import user
from Link.user.views import UserAPI
from Link.chat_session.views import ChatSessionAPI, MessageAPI

# app.register_blueprint(user)
user_view = UserAPI.as_view('user')
chat_session_view = ChatSessionAPI.as_view('chat-session')
message_view = MessageAPI.as_view('send-message')
app.add_url_rule('/user/', view_func=user_view, defaults={'id': None}, methods=['GET', 'POST'])
app.add_url_rule('/user/<id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/chat-session/', view_func=chat_session_view, defaults={'id': None}, methods=['GET', 'POST'])
app.add_url_rule('/chat-session/<id>', view_func=chat_session_view, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/chat-session/<id>/message', view_func=message_view, methods=['GET', 'POST'])
