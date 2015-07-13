__author__ = 'FindIn'

from marshmallow import Schema, fields

class TagSchema(Schema):

  id = fields.Int()
  parentId = fields.Int(attribute='parent_id')
  category = fields.Str()
  name = fields.Str()

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


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
  tags = fields.Nested(TagSchema, many=True)


user_schema = UserSchema()
users_with_tags_schema = UserSchema(many=True)


class UserTagSchema(Schema):
  user = fields.Nested(UserSchema)
  tag = fields.Nested(TagSchema)

  fields = ('user', 'tag')