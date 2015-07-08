__author__ = 'FindIn'

from marshmallow import Serializer, fields

class UserSerializer(Serializer):
  class Meta:
    fields = ("id", "profile")


class TagSerializer(Serializer):
  class Meta:
    fields = ("id", "parent_id", "category", "name", "create_time", "update_time")


class UserTagSerializer(Serializer):
  user = fields.Nested(UserSerializer)
  tag = fields.Nested(TagSerializer)

  class Meta:
    fields = ('user', 'tag', 'create_time')