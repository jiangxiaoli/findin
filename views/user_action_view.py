from models.location import Location
from serializers.location_serializers import LocationSerializer
from serializers.simgle_general_serializers import error_serializers
from flask_restful import Resource, reqparse
from server import api, db

class LocationView(Resource):

    def put(self, user_id):
        # PUT param
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('venue_id', type = str, required = True,
                                   help = 'No venue id provided', location = 'json')
        self.reqparse.add_argument('venue_name', type = str, location = 'json')
        self.reqparse.add_argument('lat', type = str, location = 'json')
        self.reqparse.add_argument('lng', type = str, location = 'json')
        args = self.reqparse.parse_args()

        # query location in table
        location = Location.query.filter_by(user_id=user_id).first()
        if location is not None:
            # update location
            location.venue_id = args['venue_id']
            location.venue_name = args['venue_name']
            location.lat = args['lat']
            location.lng = args['lng']
        else:
            # create new location
            location = Location(user_id = user_id, venue_id=args['venue_id'], venue_name=args['venue_name'], lat=args['lat'], lng=args['lng'])
            db.session.add(location)
        db.session.commit()
        return LocationSerializer(location).data

    def get(self, user_id):
        location = Location.query.filter_by(user_id=user_id).first()
        if location:
            return LocationSerializer(location).data
        else:
            return error_serializers('Unknown location!', 400), 400

api.add_resource(LocationView,'/users/<int:user_id>/location')