import datetime
from flask import jsonify
from flask.ext.restful import reqparse
import time
from models.location import Location
from models.user import User, Tag, UserTag
from schemas.user_schemas import user_schema, users_with_tags_schema, tags_schema
from serializers.simgle_general_serializers import error_serializers
from serializers.user_wish_serializers import user_wish_serializers
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
parser.add_argument('positions', type=str, location='json')
parser.add_argument('publicProfileUrl', type=str)
parser.add_argument('summary', type=str)
parser.add_argument('deviceId', type=str)

parser.add_argument('userId', type=int)
parser.add_argument('venueId', type=str)


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


  def get(self):

    args = parser.parse_args()
    if not args['venueId'] or not args['userId']:
      return error_serializers('Params Error!', 400), 400

    same_location_users = get_location_users(args['venueId'], args['userId'])

    return jsonify({"users" : users_with_tags_schema.dump(same_location_users).data})


def get_location_users(venue_id, user_id):

  same_locations = Location.query.filter(Location.venue_id == venue_id, Location.user_id != user_id,
                                         Location.create_time > (datetime.datetime.now() + datetime.timedelta(minutes=30))).all()
  same_location_users = []
  user_ids = set()

  if same_locations:
    for same_location in same_locations:
      user_ids.add(same_location.user_id)
      user = User.query.filter_by(id=same_location.user_id).first()
      tags = db.session.query(Tag).join(UserTag).filter(UserTag.user_id==same_location.user_id).all()
      user.tags = tags
      same_location_users.append(user)

  hardcode_users = User.query.filter(User.id>=62, User.id<=68).all()
  for hardcode_user in hardcode_users:
    if hardcode_user.id in user_ids:
      continue
    tags = db.session.query(Tag).join(UserTag).filter(UserTag.user_id==hardcode_user.id).all()
    hardcode_user.tags = tags
    same_location_users.append(hardcode_user)

  return same_location_users


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
    user.device_id = user_params['deviceId']
    user.update_time = time.strftime("%Y-%m-%d %X", time.localtime())

  else:
    # Add
    user = User(user_params['firstName'], user_params['lastName'], user_params['linkedinId'], user_params['headline'],
                user_params['industry'], user_params['location'], user_params['positions'], user_params['summary'],
                user_params['numberOfConnections'], user_params['publicProfileUrl'], user_params['pictureUrl'],
                '', user_params['deviceId'])
    db.session.add(user)

  db.session.commit()

  return user


def analysis_tags(user_id, params):

  try:
    if params["industry"]:
      analysis_a_tag(user_id, "industry", params["industry"])

    if params["positions"]:
      print params["positions"]
      positions = params["positions"].split()
      print positions
      print type(positions)
      if positions:
        for position in positions:
          print position
          if position["company"]:
            analysis_a_tag(user_id, "company", position["company"])

          if position["title"]:
            analysis_a_tag(user_id, "title", position["title"])

  except Exception, e:
    print 'Analysis_tags error', e.message


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

class UserWishView(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user_wish_serializers(id, user.wish)
        else:
            return error_serializers('User not found!', 404), 404

    def put(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            # PUT param
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('wish', type = str, location = 'json')
            args = self.reqparse.parse_args()
            user.wish = args['wish']
            db.session.commit()
            return user_wish_serializers(id, user.wish)
        else:
            return error_serializers('User not found!', 404), 404


class TagsView(Resource):

    def get(self):

      result = {}

      industry_tags = Tag.query.filter_by(id=1).all()
      result['industry'] = tags_schema.dump(industry_tags).data

      company_tags = Tag.query.filter_by(id=2).all()
      result['company'] = tags_schema.dump(company_tags).data
      
      title_tags = Tag.query.filter_by(id=3).all()
      result['title'] = tags_schema.dump(title_tags).data

      return result


api.add_resource(UserAddView, '/users')
api.add_resource(UserView, '/users/<int:id>')
api.add_resource(UserWishView, '/users/<int:id>/wish')
api.add_resource(TagsView, '/tags')