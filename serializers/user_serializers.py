__author__ = 'FindIn'

from marshmallow import Serializer, fields

class UserSerializer(Serializer):
  class Meta:
    fields = ("id", "first_name", "last_name", "linkedin_id", "headline", "industry", "location", "positions",
              "summary", "public_profile_url", "num_collections", "picture_url")


class TagSerializer(Serializer):
  class Meta:
    fields = ("id", "parent_id", "category", "name", "create_time", "update_time")


class UserTagSerializer(Serializer):
  user = fields.Nested(UserSerializer)
  tag = fields.Nested(TagSerializer)

  class Meta:
    fields = ('user', 'tag', 'create_time')