from Link import socketIO
from flask import request
from Link.helper.user_sid_map import set_user_sid


@socketIO.on('connect')
def test_connect():
    print("Connected")


@socketIO.on("is online")
def login_user(data):
    print("Is Online", data)
    set_user_sid(data["user"], request.sid)

