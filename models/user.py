from sqlalchemy import ForeignKey

__author__ = 'FindIn'

from flask import g
from server import db

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(64), nullable=False)
  last_name = db.Column(db.String(64), nullable=False)
  linkedin_id = db.Column(db.String(64))
  headline = db.Column(db.String(128))
  linkedin_profile_url = db.Column(db.String(256))
  picture_url = db.Column(db.String(256))
  profile = db.Column(db.Text())
  access_token = db.Column(db.String(128))
  create_time = db.Column(db.DateTime, default=db.func.now())
  update_time = db.Column(db.DateTime)

  def __init__(self, first_name, last_name, linkedin_id, headline, linkedin_profile_url,
               picture_url, profile, access_token):
    self.first_name = first_name
    self.last_name = last_name
    self.linkedin_id = linkedin_id
    self.headline = headline
    self.linkedin_profile_url = linkedin_profile_url
    self.picture_url = picture_url
    self.profile = profile
    self.access_token = access_token

  def __repr__(self):
      return '<User %r>' % self.profile


class Tag(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  parent_id = db.Column(db.Integer, ForeignKey('tag.id'))
  category = db.Column(db.String(128))
  name = db.Column(db.String(128), nullable=False, unique=True)
  create_time = db.Column(db.DateTime, default=db.func.now())
  update_time = db.Column(db.DateTime)

  def __init__(self, name):
    self.parent_id = g.tag.id
    self.category = g.tag.name
    self.name = name

  def __repr__(self):
      return '<Tag %r>' % (self.name, self.category)


class TagUser(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey('user.id'))
  tag_id = db.Column(db.Integer, ForeignKey('tag.id'))

  def __init__(self):
    self.user_id = g.user.id
    self.tag_id = g.tag.id

  def __repr__(self):
      return '<Tag %r>' % (self.user_id, self.tag_id)