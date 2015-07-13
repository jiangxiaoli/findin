__author__ = 'FindIn'

import os

from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.httpauth import HTTPBasicAuth

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

app = Flask(__name__)
app.config.from_object('config')

# flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+oursql://findin:findin123@23.228.104.59/findin"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+oursql://root:linkedin@localhost/FindIn"
db = SQLAlchemy(app)

# flask-restful
api = Api(app)

# flask-bcrypt
flask_bcrypt = Bcrypt(app)

# flask-httpauth
auth = HTTPBasicAuth()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

import views.user_view
import views.user_action_view