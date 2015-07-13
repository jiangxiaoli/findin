__author__ = 'FindIn'

from marshmallow import Schema, fields

class LocationSchema(Schema):
    id = fields.Int(dump_only=True)
    userId = fields.Str(attribute='user_id')
    venueId = fields.Str(attribute='venue_id')
    venueName = fields.Str(attribute='venue_name')
    lat = fields.Str()
    lng = fields.Str()
    createTime = fields.DateTime(dump_only=True, attribute='create_time')
    updateTime = fields.DateTime(dump_only=True, attribute='update_time')

location_schema = LocationSchema()