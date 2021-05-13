from flask import Flask
from flask_mongoengine import MongoEngine
from Link.user.models import User, Role
from flask_security import Security, MongoEngineUserDatastore
from Link.user.auth_forms import ExtendedRegisterForm
from flask_mail import Mail
from flask_cors import CORS

from flask import json
from werkzeug.exceptions import HTTPException
from .framework.error_handler import handle_http_exception, handle_all_exception


app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {'db': 'linkdb',
                                  'host': 'localhost',
                                  'port': 27017
                                  }
app.config['SECRET_KEY'] = 'Thisisasecretkey'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_API_ENABLED_METHODS'] = ['token']
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'Thisissecuritypaswordsalt'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True  # TODO: Check what this flag does
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
mail = Mail(app)
app.debug = True
app.register_error_handler(HTTPException, handle_http_exception) # TODO: We can probably remove this handler
app.register_error_handler(Exception, handle_all_exception)


db = MongoEngine(app)

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedRegisterForm)

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
