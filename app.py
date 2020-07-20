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
        set routes of the CRUD functions for an app created
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
            Create a new Character with Hat associate, following the rules
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
        #Check all the rules
        message = [rule(params) for k,rule in Character_rules.items() ]
        for b, m  in message :
            if not(b):
                return make_response(m,401)
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
   
        import json
        from rules import Character_rules

        get_character = Character.query.get(idx)
        schema = CharacterSchema()

        params = schema.dump(get_character)
        if 'Color' in request.args:
            from models import ColorHat, Hat
            Color = request.args.get('Color')
            hat = Hat(Color = Color)
            hat_schema = HatSchema()
            params['Hat'] = hat
            setattr(getattr(get_character,'Hat'),'Color',ColorHat[Color])
        else:
            params['Hat'] = None
        if 'Name' in request.args:
            Name=request.args.get('Name')
            params['Name'] = Name
            setattr(get_character,'Name',Name)
        if 'Age' in request.args:
            Age=request.args.get('Age')
            params['Age'] = json.loads(Age)
            setattr(get_character,'Age',json.loads(Age)) 
        if 'Weight' in request.args:
            Weight=request.args.get('Weight')
            params['Weight'] = json.loads(Age)
            setattr(get_character,'Weight',json.loads(Weight))
        if 'Human' in request.args:
            Human= json.loads(request.args.get('Human').lower())
            params['Human'] = Human
            setattr(get_character,'Human',Human)

        message = [rule(params) for k,rule in Character_rules.items() ]
        for b, m  in message :
            if not(b):
                return make_response(m,401)

        db.session.add(get_character)
        db.session.commit()
        character_schema =CharacterSchema()
        character = character_schema.dump(get_character)
        return make_response(jsonify({"character": character}))


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
