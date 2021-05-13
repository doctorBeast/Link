from flask import Blueprint, request, Response
from flask.views import MethodView
from .models import User
from bson import ObjectId
from Link.framework.serializer import Serializer
from flask_security import auth_token_required, current_user
import json


# user = Blueprint('user', __name__)
#
#
# @user.route('/')
# @user.route('/user')
# def get_user():
#     users = User.objects().to_json()
#     user_data = {
#         'name': 'ABC',
#         'email': 'abc@example.com'
#     }
#     user = User(**user_data)
#     user.save()
#     return Response(users, mimetype="application/json", status=200)


class UserAPI(MethodView):
    serializer = Serializer(document_cls=User)

    @auth_token_required
    def get(self, id):
        if id:
            id = ObjectId(id)
            user = User.objects().get(id=id)
            user = self.serializer.serialize(user, exclude_fields=["password", "fs_uniquifier"])
            return Response(user, mimetype="application/json", status=200)
        else:
            # This logic will get the logged In User
            user = json.dumps({
                "name": current_user.name,
                "email": current_user.email,
                "id": str(current_user.id)
            })
            return Response(user, mimetype="application/json", status=200)

    @auth_token_required
    def post(self, id):
        # read request object and fetch details
        user_data = request.get_json()
        user = User(**user_data)
        user.name = 'ABC'
        try:
            user.save()
        except Exception as e:
            raise e
        return {'id': str(user.id)}, 200

    @auth_token_required
    def put(self, id):
        user_data = request.get_json()
        User.objects(id=id).update(**user_data)
        return '', 200
        pass
