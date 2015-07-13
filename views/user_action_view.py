from models.location import Location
from models.invitation import Invitation
from models.user import User
from serializers.simgle_general_serializers import error_serializers
from schemas.invitation_schemas import invitation_schema, invitations_schema
from schemas.location_schemas import location_schema
from flask_restful import Resource, reqparse
from server import api, db
from flask import jsonify
import os

from apns import APNs, Payload

# init apns
cert_path = os.path.join(os.path.dirname(__file__), '../developmentCert.pem')
key_path = os.path.join(os.path.dirname(__file__), '../developmentKey.pem')
apns = APNs(use_sandbox=True, cert_file=cert_path, key_file=key_path)

class LocationView(Resource):

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            # PUT param
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('venueId', type = str, required = True,
                                       help = 'No venue id provided', location = 'json')
            self.reqparse.add_argument('venueName', type = str, location = 'json')
            self.reqparse.add_argument('lat', type = str, location = 'json')
            self.reqparse.add_argument('lng', type = str, location = 'json')
            args = self.reqparse.parse_args()

            # query location in table
            location = Location.query.filter_by(user_id=user_id).first()
            if location is not None:
                # update location
                location.venue_id = args['venueId']
                location.venue_name = args['venueName']
                location.lat = args['lat']
                location.lng = args['lng']
                location.update_time = db.func.now()
            else:
                # create new location
                location = Location(user_id = user_id, venue_id=args['venueId'], venue_name=args['venueName'], lat=args['lat'], lng=args['lng'])
                db.session.add(location)
            db.session.commit()

            result = location_schema.dump(Location.query.get(location.id))
            return jsonify({"location": result.data})
        else:
            return error_serializers('User not found!', 400), 400

    def get(self, user_id):
        location = Location.query.filter_by(user_id=user_id).first()
        if location:
            result = location_schema.dump(Location.query.get(location.id))
            return jsonify({"location": result.data})
        else:
            return error_serializers('Unknown location!', 400), 400

class InvitationsView(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            invitations_from_me = Invitation.query.filter_by(inviter_id=user_id)
            invitations_to_me = Invitation.query.filter_by(invitee_id=user_id)
            # Serialize the queryset
            result_invitations_from_me = invitations_schema.dump(invitations_from_me)
            result_invitations_to_me = invitations_schema.dump(invitations_to_me)
            return jsonify({'invitations_from_me': result_invitations_from_me.data, "invitations_to_me": result_invitations_to_me.data})
        else:
            return error_serializers('User not found!', 400), 400

    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            # POST param
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('inviteeId', type = str, required = True,
                                       help = 'No invitee id provided', location = 'json')
            args = self.reqparse.parse_args()

            # create new invitation
            invitation = Invitation(inviter_id = user_id, invitee_id=args['inviteeId'])
            db.session.add(invitation)
            db.session.commit()

            # notify inviter status
            # Send a notification to invitee
            invitee_id = invitation.invitee_id
            invitee = User.query.filter_by(id=invitee_id).first()
            token_hex = invitee.device_id

            if token_hex:
                #get inviter name
                inviter_id = invitation.inviter_id
                inviter = User.query.filter_by(id=inviter_id).first()
                inviter_name = inviter.first_name + " " + inviter.last_name

                alert_text = "Your got an invitation from "+ inviter_name + "!"
                payload = Payload(alert=alert_text, sound="default", badge=1)
                apns.gateway_server.send_notification(token_hex, payload)

            result = invitation_schema.dump(Invitation.query.get(invitation.id))
            return jsonify({"invitation": result.data})
        else:
            return error_serializers('User not found!', 400), 400

class InvitationView(Resource):

    def put(self, invitation_id):
        # PUT param
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('status', type = int, required = True,
                                   help = 'No status id provided', location = 'json')
        args = self.reqparse.parse_args()

        # query location in table
        invitation = Invitation.query.filter_by(id=invitation_id).first()
        if invitation is not None:
            # update invitation
            invitation.status = args['status']
            invitation.update_time = db.func.now()
            db.session.commit()

            # notify inviter status
            # Send a notification to inviter
            inviter_id = invitation.inviter_id
            inviter = User.query.filter_by(id=inviter_id).first()
            token_hex = inviter.device_id

            if token_hex:
                #get invitee name
                invitee_id = invitation.invitee_id
                invitee = User.query.filter_by(id=invitee_id).first()
                invitee_name = invitee.first_name + " " + invitee.last_mame

                if invitation.status == 2:
                    alert_text = "Your invitation to "+ invitee_name + " is accepted!"
                    payload = Payload(alert=alert_text, sound="default", badge=1)
                    apns.gateway_server.send_notification(token_hex, payload)

            result = invitation_schema.dump(Invitation.query.get(invitation.id))
            return jsonify({"invitation": result.data})
        else:
            return error_serializers('Unknown invitation!', 400), 400

    def get(self, invitation_id):
        invitation = Invitation.query.filter_by(id=invitation_id).first()
        if invitation:
            result = invitation_schema.dump(Invitation.query.get(invitation.id))
            return jsonify({"invitation": result.data})
        else:
            return error_serializers('Unknown invitation!', 400), 400

api.add_resource(LocationView,'/users/<int:user_id>/location')
api.add_resource(InvitationsView,'/users/<int:user_id>/invitations')
api.add_resource(InvitationView,'/invitations/<int:invitation_id>')