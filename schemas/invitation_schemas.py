__author__ = 'FindIn'

from marshmallow import Schema, fields
from schemas.user_schemas import UserSchema

class InvitationSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Int()
    createTime = fields.DateTime(dump_only=True, attribute='create_time')
    updateTime = fields.DateTime(dump_only=True, attribute='update_time')
    inviter = fields.Nested(UserSchema)
    invitee = fields.Nested(UserSchema)

invitation_schema = InvitationSchema()
invitations_schema = InvitationSchema(many=True)