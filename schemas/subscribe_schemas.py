__author__ = 'FindIn'

from marshmallow import Schema, fields
from schemas.user_schemas import UserSchema

class SubscribeSchema(Schema):
    id = fields.Int(dump_only=True)
    tags = fields.Str()
    createTime = fields.DateTime(dump_only=True, attribute='create_time')
    updateTime = fields.DateTime(dump_only=True, attribute='update_time')
    user = fields.Nested(UserSchema)

subscribe_schema = SubscribeSchema()
