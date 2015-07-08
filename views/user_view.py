from models.user import User
from serializers.serializers import UserSerializer
from flask_restful import Resource
from server import api


class UserView(Resource):

  def get(self, id):
    user = User.query.filter_by(id=id).first()
    return UserSerializer(user).data


api.add_resource(UserView, '/users/<int:id>')