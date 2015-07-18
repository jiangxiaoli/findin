__author__ = 'FindIn'

from sqlalchemy import ForeignKey
from server import db

class Subscribe(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=1)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    tags = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.now())
    update_time = db.Column(db.DateTime)
    user = {}

    def __init__(self, user_id, tags):
        self.user_id = user_id
        self. tags = tags

    def __repr__(self):
        return '<Subscribe %r>' % (self.id, self.user_id, self.tags)