from sqlalchemy import ForeignKey

__author__ = 'FindIn'

from server import db

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=1)
  first_name = db.Column(db.String(64), nullable=False)
  last_name = db.Column(db.String(64), nullable=False)
  linkedin_id = db.Column(db.String(64))
  headline = db.Column(db.String(128))
  industry = db.Column(db.String(128))
  location = db.Column(db.String(128))
  positions = db.Column(db.Text())
  summary = db.Column(db.String(512))
  num_collections = db.Column(db.Integer)
  public_profile_url = db.Column(db.String(256))
  picture_url = db.Column(db.String(256))
  wish = db.Column(db.String(256))
  device_id = db.Column(db.String(256))
  create_time = db.Column(db.DateTime, default=db.func.now())
  update_time = db.Column(db.DateTime)

  def __init__(self, first_name, last_name, linkedin_id, headline, industry, location,
               positions, summary, num_collections, public_profile_url, picture_url, wish, device_id):
    self.first_name = first_name
    self.last_name = last_name
    self.linkedin_id = linkedin_id
    self.headline = headline
    self.picture_url = picture_url
    self.industry = industry
    self.location = location
    self.positions = positions
    self.summary = summary
    self.num_collections = num_collections
    self.public_profile_url = public_profile_url
    self.wish = wish
    self.device_id = device_id

  def __repr__(self):
      return '<User %r>' % self.linkedin_id


class Tag(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=1)
  parent_id = db.Column(db.Integer, ForeignKey('tag.id'))
  category = db.Column(db.String(128))
  name = db.Column(db.String(128), nullable=False, unique=True)
  create_time = db.Column(db.DateTime, default=db.func.now())
  update_time = db.Column(db.DateTime)

  def __init__(self, parent_id, category, name):
    self.parent_id = parent_id
    self.category = category
    self.name = name

  def __repr__(self):
      return '<Tag %r>' % (self.name, self.category)


class UserTag(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=1)
  user_id = db.Column(db.Integer, ForeignKey('user.id'))
  tag_id = db.Column(db.Integer, ForeignKey('tag.id'))

  def __init__(self, user_id, tag_id):
    self.user_id = user_id
    self.tag_id = tag_id

  def __repr__(self):
      return '<Tag %r>' % (self.user_id, self.tag_id)