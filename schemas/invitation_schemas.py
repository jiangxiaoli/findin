__author__ = 'FindIn'

from marshmallow import Schema, fields
from schemas.user_schemas import UserSchema

class InvitationSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str()
    createTime = fields.DateTime(dump_only=True, attribute='create_time')
    updateTime = fields.DateTime(dump_only=True, attribute='update_time')
    inviter = fields.Nested(UserSchema, only=["id", "firstName", "lastName", "headline", "public_profile_url"])
    invitee = fields.Nested(UserSchema, only=["id", "firstName", "lastName", "headline", "public_profile_url"])

invitation_schema = InvitationSchema()
invitations_schema = InvitationSchema(many=True)