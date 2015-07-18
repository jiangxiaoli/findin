from models.location import Location
from models.invitation import Invitation
from models.user import User
from models.subscribe import Subscribe
from schemas.user_schemas import users_with_tags_schema
from serializers.simgle_general_serializers import error_serializers
from schemas.invitation_schemas import invitation_schema, invitations_schema
from schemas.location_schemas import location_schema
from schemas.subscribe_schemas import subscribe_schema
from flask_restful import Resource, reqparse
from server import api, db
from flask import jsonify
import os

from apns import APNs, Payload

# init apns
from views.user_view import get_location_users

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
            location_query = Location.query.filter_by(user_id=user_id)
            if location_query.first():
                # update location
                location = location_query.scalar()
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

            same_location_users = get_location_users(args['venueId'], user_id)

            return jsonify({"users" : users_with_tags_schema.dump(same_location_users).data})
        else:
            return error_serializers('User not found!', 404), 404

    def get(self, user_id):
        location = Location.query.filter_by(user_id=user_id).first()
        if location:
            result = location_schema.dump(Location.query.get(location.id))
            return jsonify({"location": result.data})
        else:
            return error_serializers('Unknown location!', 404), 404

class InvitationsView(Resource):

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        invitations_from_me_arr = []
        invitations_to_me_arr = []

        if user:
            invitations_from_me = Invitation.query.filter_by(inviter_id=user_id)
            for invitationFrom in invitations_from_me:
                inviter = User.query.filter_by(id=invitationFrom.inviter_id).first()
                invitationFrom.inviter = inviter
                invitee = User.query.filter_by(id=invitationFrom.invitee_id).first()
                invitationFrom.invitee = invitee
                invitations_from_me_arr.append(invitationFrom)

            invitations_to_me = Invitation.query.filter_by(invitee_id=user_id)
            for invitationTo in invitations_to_me:
                inviter = User.query.filter_by(id=invitationTo.inviter_id).first()
                invitationTo.inviter = inviter
                invitee = User.query.filter_by(id=invitationTo.invitee_id).first()
                invitationTo.invitee = invitee
                invitations_to_me_arr.append(invitationTo)

            # Serialize the queryset
            result_invitations_from_me = invitations_schema.dump(invitations_from_me_arr)
            result_invitations_to_me = invitations_schema.dump(invitations_to_me_arr)
            return jsonify({'invitationsFromMe': result_invitations_from_me.data, "invitationsToMe": result_invitations_to_me.data})
        else:
            return error_serializers('User not found!', 404), 404

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
            return error_serializers('User not found!', 404), 404

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
                invitee_name = invitee.first_name + " " + invitee.last_name

                if invitation.status == 2:
                    alert_text = "Your invitation to "+ invitee_name + " is accepted!"
                    payload = Payload(alert=alert_text, sound="default", badge=1)
                    apns.gateway_server.send_notification(token_hex, payload)

            result = invitation_schema.dump(Invitation.query.get(invitation.id))
            return jsonify({"invitation": result.data})
        else:
            return error_serializers('Unknown invitation!', 404), 404

    def get(self, invitation_id):
        invitation = Invitation.query.filter_by(id=invitation_id).first()
        if invitation:
            result = invitation_schema.dump(Invitation.query.get(invitation.id))
            return jsonify({"invitation": result.data})
        else:
            return error_serializers('Unknown invitation!', 404), 404

class UserSubAddView(Resource):
    def post(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            # POST param
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('tags', type = str, location = 'json')
            args = self.reqparse.parse_args()
            subscribe = Subscribe(id, args['tags'])
            subscribe.user = user
            db.session.add(subscribe)
            db.session.commit()
            result = subscribe_schema.dump(subscribe.query.get(subscribe.id))
            return jsonify({"subscribe": result.data})
        else:
            return error_serializers('User not found!', 404), 404

class UserSubView(Resource):
    def put(self, id, sub_id):
        user = User.query.filter_by(id=id).first()
        subscribe = Subscribe.query.filter_by(id=sub_id).first()
        if user and subscribe:
            # PUT param
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('tags', type = str, location = 'json')
            args = self.reqparse.parse_args()
            subscribe.tags = args['tags']
            subscribe.user = user
            db.session.commit()
            result = subscribe_schema.dump(subscribe.query.get(subscribe.id))
            return jsonify({"subscribe": result.data})
        else:
            return error_serializers('Record not found!', 404), 404

    def get(self, id, sub_id):
        user = User.query.filter_by(id=id).first()
        subscribe = Subscribe.query.filter_by(id=sub_id).first()
        if user and subscribe:
            subscribe.user = user
            result = subscribe_schema.dump(subscribe)
            return jsonify({"subscribe": result.data})
        else:
            return error_serializers('Record not found!', 404), 404

api.add_resource(LocationView,'/users/<int:user_id>/location')
api.add_resource(InvitationsView,'/users/<int:user_id>/invitations')
api.add_resource(InvitationView,'/invitations/<int:invitation_id>')
api.add_resource(UserSubAddView, '/users/<int:id>/subscribe')
api.add_resource(UserSubView, '/users/<int:id>/subscribe/<int:sub_id>')