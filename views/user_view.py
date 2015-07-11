import urllib2
from flask import json
from flask.ext.restful import reqparse
from models.user import User
from serializers.simgle_general_serializers import error_serializers
from serializers.user_serializers import UserProfileSerializer
from flask_restful import Resource
from server import api, db

REQUEST_URL = 'https://api.linkedin.com/v1/people/~:' \
              '(id,first-name,last-name,headline,skills,educations,positions,picture-url,siteStandardProfileRequest)' \
              '?oauth2_access_token=%s&format=json'

class UserView(Resource):

  def get(self, id):

    user = User.query.filter_by(id=id).first()

    if user:
      return UserProfileSerializer(user).data

    else:
      return error_serializers('Unknown user!', 400), 400

parser = reqparse.RequestParser()
parser.add_argument('access_token', type=str)

class UserAddView(Resource):

  def post(self):

    args = parser.parse_args()

    if not args['access_token']:
      return error_serializers('Unknown params!', 400), 400

    # Request linkedin profile according access_token
    profile = request_linkedin_user_content(args['access_token'])

    # Add user or update user in our database
    if(profile):
      user = add_or_update_user(profile, args['access_token'])

      if user:
        return UserProfileSerializer(user).data

      else:
        return error_serializers('Error token!', 401), 401
    else:
      return error_serializers('Error token!', 401), 401


def add_or_update_user(profile, access_token):

  profile_map = json.loads(profile)
  user = User.query.filter_by(linkedin_id=profile_map['id']).first()

  if user:
    # Update
    user = User.query.filter_by(id=user.id).scalar()
    user.first_name = profile_map['firstName']
    user.last_name = profile_map['lastName']
    user.headline = profile_map['headline']
    user.linkedin_profile_url = '' if not profile_map['siteStandardProfileRequest'] else profile_map['siteStandardProfileRequest']['url']
    user.picture_url = profile_map['pictureUrl']
    user.profile = profile
    user.access_token = access_token

  else:
    # Add
    user = User(profile_map['firstName'], profile_map['lastName'], profile_map['id'], profile_map['headline'],
               '' if not profile_map['siteStandardProfileRequest'] else profile_map['siteStandardProfileRequest']['url'],
                profile_map['pictureUrl'], profile, access_token)
    db.session.add(user)

  db.session.commit()

  return user

def request_linkedin_user_content(access_token):

  headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

  try:
    req = urllib2.Request(REQUEST_URL % access_token, headers=headers)
    return unicode(urllib2.urlopen(req, timeout=20).read(), 'utf-8')

  except Exception, e:
    print 'http request_linkedin_user_content error: ', access_token, e
    return None


api.add_resource(UserAddView, '/users')
api.add_resource(UserView, '/users/<int:id>/linkedin_profile')