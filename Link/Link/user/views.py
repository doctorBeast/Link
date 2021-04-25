from flask import Blueprint, request, Response
from flask.views import MethodView
from .models import User
from bson import ObjectId


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

    def get(self, id):
        if id:
            id = ObjectId(id)
            user = User.objects().get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        else:
            users = User.objects().to_json()
            return Response(users, mimetype="application/json", status=200)

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

    def put(self, id):
        user_data = request.get_json()
        User.objects(id=id).update(**user_data)
        return '', 200
        pass

