__author__ = 'FindIn'

from marshmallow import Serializer, fields

class UserProfileSerializer(Serializer):
  class Meta:
    fields = ("id", "first_name")


class TagSerializer(Serializer):
  class Meta:
    fields = ("id", "parent_id", "category", "name", "create_time", "update_time")


class UserTagSerializer(Serializer):
  user = fields.Nested(UserProfileSerializer)
  tag = fields.Nested(TagSerializer)

  class Meta:
    fields = ('user', 'tag', 'create_time')