from flask import json, session
from flask.ext.restful import reqparse
from models.user import User
from serializers.simgle_general_serializers import error_serializers
from serializers.user_serializers import UserSerializer
from flask_restful import Resource
from server import api, db

class UserView(Resource):

  def get(self, id):

    user = User.query.filter_by(id=id).first()

    if user:
      return UserSerializer(user).data

    else:
      return error_serializers('Unknown user!', 400), 400

parser = reqparse.RequestParser()
parser.add_argument('linkedinId', type=str)
parser.add_argument('firstName', type=str)
parser.add_argument('headline', type=str)
parser.add_argument('industry', type=str)
parser.add_argument('lastName', type=str)
parser.add_argument('numCollections', type=int)
parser.add_argument('location', type=str)
parser.add_argument('pictureUrl', type=str)
parser.add_argument('positions', type=str)
parser.add_argument('publicProfileUrl', type=str)
parser.add_argument('summary', type=str)

class UserAddView(Resource):

  def post(self):

    args = parser.parse_args()

    if not args['firstName'] or not args['lastName'] or not args['linkedinId']:
      return error_serializers('Params Error!', 400), 400

    # Add user or update user in our database
    user = add_or_update_user(args)

    if user:
      return UserSerializer(user).data

    else:
      return error_serializers('Error token!', 401), 401


def add_or_update_user(user_params):

  query = User.query.filter_by(linkedin_id=user_params['linkedinId'])

  if query.first():
    # Update
    user = query.scalar()
    user.first_name = user_params['firstName']
    user.last_name = user_params['lastName']
    user.linkedin_id = user_params['linkedinId']
    user.headline = user_params['headline']
    user.industry = user_params['industry']
    user.location = user_params['location']
    user.positions = user_params['positions']
    user.summary = user_params['summary']
    user.num_collections = user_params['numCollections']
    user.public_profile_url = user_params['publicProfileUrl']
    user.picture_url = user_params['pictureUrl']

  else:
    # Add
    user = User(user_params['firstName'], user_params['lastName'], user_params['linkedinId'], user_params['headline'],
                user_params['industry'], user_params['location'], user_params['positions'], user_params['summary'],
                user_params['numCollections'], user_params['publicProfileUrl'], user_params['pictureUrl'])
    db.session.add(user)

  db.session.commit()

  return user


api.add_resource(UserAddView, '/users')
api.add_resource(UserView, '/users/<int:id>/linkedin_profile')