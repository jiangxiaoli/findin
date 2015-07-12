from flask import json, jsonify
from flask.ext.restful import reqparse
import time
from models.user import User, Tag, UserTag
from schemas.user_schemas import user_schema
from serializers.simgle_general_serializers import error_serializers
from flask_restful import Resource
from server import api, db

class UserView(Resource):

  def get(self, id):

    user = User.query.filter_by(id=id).first()

    if user:
      return jsonify(user_schema.dump(user).data)

    else:
      return error_serializers('Unknown user!', 400), 400

parser = reqparse.RequestParser()
parser.add_argument('linkedinId', type=str)
parser.add_argument('firstName', type=str)
parser.add_argument('headline', type=str)
parser.add_argument('industry', type=str)
parser.add_argument('lastName', type=str)
parser.add_argument('numberOfConnections', type=int)
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

    # Analysis user tags
    analysis_tags(user.id, args)

    if user:
      return jsonify(user_schema.dump(user).data)

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
    user.num_collections = user_params['numberOfConnections']
    user.public_profile_url = user_params['publicProfileUrl']
    user.picture_url = user_params['pictureUrl']
    user.update_time = time.strftime("%Y-%m-%d %X", time.localtime())

  else:
    # Add
    user = User(user_params['firstName'], user_params['lastName'], user_params['linkedinId'], user_params['headline'],
                user_params['industry'], user_params['location'], user_params['positions'], user_params['summary'],
                user_params['numberOfConnections'], user_params['publicProfileUrl'], user_params['pictureUrl'])
    db.session.add(user)

  db.session.commit()

  return user


def analysis_tags(user_id, params):

  if params["industry"]:
    analysis_a_tag(user_id, "industry", params["industry"])

  # if params["positions"]:
  #   positions = json.loads(params["positions"])
  #   if positions:
  #     for position in positions:
  #
  #       if position["company"]:
  #         analysis_a_tag(user_id, "company", position["company"])
  #
  #       if position["title"]:
  #         analysis_a_tag(user_id, "title", position["title"])


def analysis_a_tag(user_id, tag_category, tag_name):

  parent_tag = Tag.query.filter_by(name=tag_category).first()

  if not parent_tag:
    parent_tag = Tag(None, None, tag_category)
    db.session.add(parent_tag)
    db.session.commit()

  tag_query = Tag.query.filter_by(name=tag_name)

  if tag_query.first():
    tag = tag_query.first()

  else:
    tag = Tag(parent_tag.id, parent_tag.name, tag_name)
    db.session.add(tag)
    db.session.commit()

  tag_user_query = UserTag.query.filter_by(user_id=user_id, tag_id=tag.id)

  if not tag_user_query.first():
    db.session.add(UserTag(user_id, tag.id))
    db.session.commit()


api.add_resource(UserAddView, '/users')
api.add_resource(UserView, '/users/<int:id>/linkedin_profile')