__author__ = 'FindIn'

from marshmallow import Schema, fields

class InvitationSchema(Schema):
    id = fields.Int(dump_only=True)
    inviter_id = fields.Str()
    invitee_id = fields.Str()
    status = fields.Str()
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)

invitation_schema = InvitationSchema()
invitations_schema = InvitationSchema(many=True)