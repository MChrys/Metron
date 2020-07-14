import os 

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from schema import CharacterSchema, HatSchema
from models import Character, Hat
from flask_marshmallow import Marshmallow

from init_app import app , db , ma
#app = Flask(__name__)


#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

def create_app(app , db,config=None):

    @app.route('/create/', method = ['POST'])
    def add(table):
        from rules import Character_rules

        character_schema = CharacterSchema()

        Name=request.args.get('Name')
        Age=request.args.get('Age')
        Weight=request.args.get('Weight')
        Human= bool(request.args.get('Human'))
        if 'Color' in request.args:
            from models import ColorHat, Hat

            Color = request.args.get('Color')
            hat = Hat(Color = Color)
            hat_schema = HatSchema()
            params = {
                'Name' : Name,
                'Age' : Age,
                'Weight' : Weight ,
                'Human' : Human,
                'Hat' : hat
            }
            assert Character_rules['Hat'](params)
            #hat = hat_schema.load({'Color' : Color})
            result_hat = hat_schema.dump(hat.create())

        else:
            params = {
                'Name' : Name,
                'Age' : Age,
                'Weight' : Weight ,
                'Human' : Human
            }
            
        assert Character_rules['Age'](params)

        try: 
            #character = character_schema.load(params)
            character = Character(**params)
            result_character = character_schema.dump(character.create())
            return make_response(jsonify({'character': result_character}),200)

        except Exception as e:
            raise str(e) 
    
    @app.route('/read/', methods= ['GET'])
    def get_all_characters():
        try:
            get_characters = Character.query.all()
            character_schema = CharacterSchema(many=True)
            characters = character_schema.dump(get_characters)
            return make_response(jsonify({"character": characters}))
        except Exception as e:
            raise str(e)

    @app.route('/update/<idx>', methods=['PUT'])
    def update(table , idx):
        try:
            data = request.get_json()
            get_character = Character.query.get(id)
            for k, v in data.items():
                setattr(get_character,k,v)
            db.session.add(get_character)
            db.session.commit()
            character_schema =CharacterSchema()
            character = character_schema.dump(get_character)
            return make_response(jsonify({"character": character}))

        except Exception as e:
            raise str(e)

    @app.route('/delete/<idx>', methods= ['DELETE'])
    def delete(table, idx):
        try:
            get_character = Character.query.get(idx)
            db.session.delete(get_character)
            db.session.commit()
            return make_response('',204)
        except Exception as e:
            raise str(e)
    return app

if __name__ == "__main__":
    app  =create_app(app, db)
    app.run(debug=True, host='0.0.0.0')