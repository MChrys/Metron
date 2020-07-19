import os 

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from schema import CharacterSchema, HatSchema
from models import Character, Hat, ColorHat
from flask_marshmallow import Marshmallow
import json
from init_app import app , db , ma


def set_route(app, db):
    '''
    Description : 
        set routes of the CRUD function in app created
        in ini_app.py
    '''
    @app.route('/')
    @app.route('/index', methods = ['GET'])
    def welcome():
        return 'hello Metron'

    @app.route('/create', methods = ['POST'])
    def add():
        '''
        Description :
            Create a new character with 
        Example :
            >>> request.post(/create?Name=Alain&Age=18&Weight=80
            /   &Human=True&Color=YELLOW)

        '''

        from rules import Character_rules

        character_schema = CharacterSchema()

        Name=request.args.get('Name')
        Age=request.args.get('Age')
        Weight=request.args.get('Weight')
        Human= json.loads(request.args.get('Human').lower())

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
            
            #hat = hat_schema.load({'Color' : Color})
            result_hat = hat_schema.dump(hat.create())

        else:
            params = {
                'Name' : Name,
                'Age' : Age,
                'Weight' : Weight ,
                'Human' : Human,
                'Hat': None
            }
        #Check all rules
        message = [rule(params) for k,rule in Character_rules.items() ]
        for b, m  in message :
            if not(b):
                return make_response(m,401)
        #assert Character_rules['Hat'](params)
        #assert Character_rules['Age'](params)
        try:
            #character = character_schema.load(params)
            character = Character(**params)
            result_character = character_schema.dump(character.create())
            return make_response(jsonify({'character': result_character}),200)

        except Exception as e:
            raise str(e) 

    @app.route('/read_all', methods= ['GET'])
    def get_all_characters():
        try:
            get_characters = Character.query.all()
            character_schema = CharacterSchema(many=True)
            characters = character_schema.dump(get_characters)
            return make_response(jsonify({"characters": characters}),202)
        except Exception as e:
            raise str(e)

    @app.route('/read/<idx>', methods= ['GET'])
    def get_character(idx):
        try:
            get_characters = Character.query.get(idx)
            character_schema = CharacterSchema()
            characters = character_schema.dump(get_characters)
            return make_response(jsonify({"character": characters}),202)
        except Exception as e:
            raise str(e)


    @app.route('/update/<idx>', methods=['PUT'])
    def update(idx):
        try:
            data = request.get_json()
            get_character = Character.query.get(idx)
            print(get_character)
            for k, v in data.items():
                #assert k in get_character.keys() , "{} doesn't define Character Schema"
                if k == 'Color':
                    print('COLOR HAT DUMPS', json.dumps(ColorHat[k]))
                    get_character['Hat']['Color']= json.dumps(ColorHat[k])
                else: 
                    setattr(get_character,k,v)
            #chara = CharacterSchema()
            #params = chara.dump()

            message = [rule(get_character) for k,rule in Character_rules.items() ]
            for b, m  in message :
                if not(b):
                    return make_response(m,401)
            #assert Character_rules['Hat'](params)
            #assert Character_rules['Age'](params)
            db.session.add(get_character)
            db.session.commit()
            character_schema =CharacterSchema()
            character = character_schema.dump(get_character)
            return make_response(jsonify({"character": character}))

        except Exception as e:
            raise str(e)

    @app.route('/delete/<idx>', methods= ['DELETE'])
    def delete(idx):
        try:
            get_character = Character.query.get(idx)
            db.session.delete(get_character)
            db.session.commit()
            return make_response('',202)
        except Exception as e:
            raise str(e)

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404
    return app, db

app, db = set_route(app, db)

if __name__ == "__main__":
    
    app.run(debug=False, host='0.0.0.0', port=5000)