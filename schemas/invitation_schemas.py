__author__ = 'FindIn'

from marshmallow import Schema, fields

class InvitationSchema(Schema):
    id = fields.Int(dump_only=True)
    inviterId = fields.Str(attribute='inviter_id')
    inviteeId = fields.Str(attribute='invitee_id')
    status = fields.Str()
    createTime = fields.DateTime(dump_only=True, attribute='create_time')
    updateTime = fields.DateTime(dump_only=True, attribute='update_time')

invitation_schema = InvitationSchema()
invitations_schema = InvitationSchema(many=True)