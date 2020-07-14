import os 

from flask import Flask, jsonify
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from schema import CharacterSchema, HatSchema
#app = Flask(__name__)


#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

def create_app(config=None):
    app = Flask(__name__)


    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    @app.route('/create', method = ['POST'])
    def add(table):
        from rules import Character_rules

        Name=request.args.get('Name')
        Age=request.args.get('Age')
        Weight=request.args.get('Weight')
        Human= bool(request.args.get('Human'))
        if 'Color' in request.args:
            from models import ColorHat, Hat

            Color = request.args.get('Color')
            hat = Hat(Color = getattr(ColorHat,Color))

            param = {
                'Name' : Name,
                'Age' : Age,
                'Weight' : Weight ,
                'Human' : Human,
                'Hat' : hat
            }
            assert Character_rules['Hat'](params)

        else:
            param = {
                'Name' : Name,
                'Age' : Age,
                'Weight' : Weight ,
                'Human' : Human
            }
            
        assert Character_rules['Age'](params)
    
        try: pass
        except Exception as e:
            raise str(e) 
    
    @app.route('/read', methods= ['GET'])
    def get_all_characters():
        get_characters = Character.query.all()
        character_schema = CharacterSchema(many=True)
        characters = character_schema.dump(get_characters)
        return make_response(jsonify({"character": characters}))

    @app.route('/update/<table>/<idx>')
    def update(table , idx):
        if table == 'Character':
            #id 
            pass
        elif table == 'Hat':
            pass
        else:
            raise KeyError("This Table doesn't exist") 

    @app.route('/delete/<table>/<idx>')
    def delete(table, idx):
        if table == 'Character':
            #id 
            pass
        else:
            raise KeyError("This Table doesn't exist") 

    return app, db

if __name__ == "__main__":
    app , db =create_app()
    app.run(debug=True, host='0.0.0.0')