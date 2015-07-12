__author__ = 'FindIn'

from marshmallow import Schema, fields

class UserSchema(Schema):

  id = fields.Int()
  firstName = fields.Str(attribute='first_name')
  lastName = fields.Str(attribute='last_name')
  linkedinId = fields.Str(attribute='linkedin_id')
  headline = fields.Str()
  industry = fields.Str()
  location = fields.Str()
  positions = fields.Str()
  summary = fields.Str()
  publicProfileUrl = fields.Str(attribute='public_profile_url')
  numOfCollections = fields.Int(attribute='num_collections')
  pictureUrl = fields.Str(attribute='picture_url')
  wish = fields.Str()
  deviceId = fields.Str(attribute='device_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class TagSchema(Schema):

  parentId = fields.Int(attribute='parent_id')
  fields = ("id", "category", "name")

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


class UserTagSchema(Schema):
  user = fields.Nested(UserSchema)
  tag = fields.Nested(TagSchema)

  fields = ('user', 'tag')
