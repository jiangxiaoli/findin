from models.location import Location
from models.invitation import Invitation
from serializers.location_serializers import LocationSerializer
from serializers.simgle_general_serializers import error_serializers
from schemas.invitation_schemas import invitation_schema, invitations_schema
from flask_restful import Resource, reqparse
from server import api, db
from flask import jsonify

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


class InvitationsView(Resource):
    def get(self, user_id):
        invitations_from_me = Invitation.query.filter_by(inviter_id=user_id)
        invitations_to_me = Invitation.query.filter_by(invitee_id=user_id)
        # Serialize the queryset
        result_invitations_from_me = invitations_schema.dump(invitations_from_me)
        result_invitations_to_me = invitations_schema.dump(invitations_to_me)
        return jsonify({'invitations_from_me': result_invitations_from_me.data, "invitations_to_me": result_invitations_to_me.data})

api.add_resource(LocationView,'/users/<int:user_id>/location')
api.add_resource(InvitationsView,'/users/<int:user_id>/invitations')