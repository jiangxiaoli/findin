from sqlalchemy import ForeignKey

__author__ = 'FindIn'

from server import db

class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=1)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    venue_id = db.Column(db.String(64), nullable=False)
    venue_name = db.Column(db.String(64))
    lat = db.Column(db.String(64))
    lng = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=db.func.now())
    update_time = db.Column(db.DateTime)

    def __init__(self, user_id, venue_id, venue_name, lat, lng):
        self.user_id = user_id
        self.venue_id = venue_id
        self.venue_name = venue_name
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return '<Location %r>' % (self.user_id, self.venue_id, self.venue_name)