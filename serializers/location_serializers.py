__author__ = 'FindIn'

from marshmallow import Serializer, fields

class LocationSerializer(Serializer):
    class Meta:
        fields = ("id", "user_id", "venue_id", "venue_name", "lat", "lng", "create_time", "update_time")