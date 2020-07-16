import os 

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from schema import CharacterSchema, HatSchema
from models import Character, Hat, ColorHat
from flask_marshmallow import Marshmallow
import json
from init_app import app , db , ma
#app = Flask(__name__)


#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)


#@app.route('/', methods = ['GET'])
@app.route('/index/', methods = ['GET'])
def welcome():
    return 'hello Metron'

@app.route('/testup', methods = ['POST','GET'])
def testup():
    if request.method =='POST':
        print('POST ------->')
        a= request.args.to_dict()
        print('request.get_json() ->',a)
        print(json.dumps([{'color':'test'}]))
        try:
            return json.dumps([a]) 
        except Exception as e:
            print(str(e))

    else:
        print('GET ------->') 
        return 'database'


@app.route('/create/', methods = ['POST'])
def add():
    try:
        from rules import Character_rules

        character_schema = CharacterSchema()

        Name=request.args.get('Name')
        Age=request.args.get('Age')
        Weight=request.args.get('Weight')
        Human= json.loads(request.args.get('Human').lower())
        print('human', Human)
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
        assert Character_rules['Hat'](params)
        assert Character_rules['Age'](params)

     
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
        return make_response(jsonify({"character": characters}),202)
    except Exception as e:
        raise str(e)

@app.route('/update/<idx>', methods=['PUT'])
def update( idx):
    try:
        data = request.get_json()
        get_character = Character.query.get(id)
        print(get_character)
        for k, v in data.items():
            #assert k in get_character.keys() , "{} doesn't define Character Schema"
            if k == 'Color':
                print('COLOR HAT DUMPS', json.dumps(ColorHat[k]))
                get_character['Hat']['Color']= json.dumps(ColorHat[k])
            else: 
                setattr(get_character,k,v)
            

        assert Character_rules['Hat'](params)
        assert Character_rules['Age'](params)
        db.session.add(get_character)
        db.session.commit()
        character_schema =CharacterSchema()
        character = character_schema.dump(get_character)
        return make_response(jsonify({"character": character}))

    except Exception as e:
        raise str(e)

@app.route('/delete/<idx>', methods= ['DELETE'])
def delete( idx):
    try:
        get_character = Character.query.get(idx)
        db.session.delete(get_character)
        db.session.commit()
        return make_response('',204)
    except Exception as e:
        raise str(e)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)