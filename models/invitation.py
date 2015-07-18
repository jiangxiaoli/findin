__author__ = 'FindIn'

from sqlalchemy import ForeignKey
from server import db

class Invitation(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=1)
    inviter_id = db.Column(db.Integer, ForeignKey('user.id'))
    invitee_id = db.Column(db.Integer, ForeignKey('user.id'))
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.now())
    update_time = db.Column(db.DateTime)
    inviter = {}
    invitee = {}

    def __init__(self, inviter_id, invitee_id):
        self.inviter_id = inviter_id
        self. invitee_id = invitee_id
        self.status = 1 # 1. not send; 2. pending, send; 3. accept; 4. deny; 5. pass

    def __repr__(self):
        return '<Invitation %r>' % (self.id, self.inviter_id, self.invitee_id, self.status)