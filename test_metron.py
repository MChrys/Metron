

import pytest

from init_app import create_app, db, app
#from config import config
from schema import HatSchema, CharacterSchema
from models import Hat, Character
@pytest.fixture(scope='module')
def test_client():
    test_app, _, __ = create_app()
    testing_client = test_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = test_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    #db = SQLAlchemy()
    # Create the database and the database table
    try :
        db.create_all()
    
        # Insert user data
        data = {'Name' :'Dog','Age':5, 'Weight':60,'Human':False,'Hat': None}
        #chara1 = CharacterSchema(Name='Alain',Age=18,Weight=80,Human=True&Color=YELLOW)
        
        character_schema = CharacterSchema()
        chara1 = Character(**data)
        #chara1 = product_schema.load(data)
        #result = character_schema.dump(chara1.create())
        #return make_response(jsonify({"character": result}),200)
        #chara2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
        db.session.add(chara1)
        #db.session.add(user2)
    
        # Commit the changes for the users
        db.session.commit()
    
        yield db  # this is where the testing happens!
    
        db.drop_all()
    except Exception as e :
        raise str(e)



def test_index(test_client, init_database):
    res =test_client.get("/")
    print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"Hello Metron" in res.data


def test_create(test_client, init_database):
    res = test_client.post("/create?Name=Alain&Age=18&Weight=80&Human=True&Color=YELLOW")
    assert res.status_code == 200
    print(res.data)
    #assert b"12345" in res.data
    