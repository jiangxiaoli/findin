from models.user import User
from serializers.simgle_general_serializers import error_serializers
from serializers.user_serializers import UserProfileSerializer
from flask_restful import Resource
from server import api


class UserView(Resource):

  def get(self, id):

    user = User.query.filter_by(id=id).first()

    if user:
      return UserProfileSerializer(user).data

    else:
      return error_serializers('Unknow user!', 400), 400


api.add_resource(UserView, '/user/<int:id>/linkedin_profile')