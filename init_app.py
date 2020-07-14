import os 

from flask import Flask, jsonify
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from schema import CharacterSchema, HatSchema
from models import Character, Hat
from flask_marshmallow import Marshmallow    
    
app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow