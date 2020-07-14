
from models import *
from marshmallow_enum import EnumField

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields



class HatSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Hat
        sqla_session = db.session
    Id = fields.Number(dump_only=True)
    Color = EnumField(ColorHat,by_value = True)

class CharacterSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Character
        sqla_session = db.session
    Id = fields.Number(dump_only=True)
    Name = fields.String(required=True)
    Age = fields.String(required=True)
    Weight = fields.String(required=True)
    Human = fields.Boolean(required=True)
    Hat = ModelSchema.Nested(HatSchema,required=False, many= False)




