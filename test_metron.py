

import pytest

from app.app import app, db
#from config import config
import pprint
import sys
pprint.pprint(sys.path)
from schema import HatSchema, CharacterSchema
from models import Hat, Character
@pytest.fixture(scope='module')
def test_client():
    test_app = app 
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
    db.session.close()
    db.drop_all()




def test_index(test_client):
    res =test_client.get("/index")
    #print(dir(res), res.status_code)
    assert res.status_code == 200
    #print(res.data)
    assert b"hello Metron" in res.data


def test_create(test_client):
    res = test_client.post("/create?Name=Alain&Age=18&Weight=80&Human=True&Color=YELLOW")
    assert res.status_code == 200
    print('RESDATA',type(res.data),res.data)
    assert b'Age":18' in res.data
    assert b'"Human":true' in res.data
    assert b'"Name":"Alain","Weight":80' in res.data
    assert b'"Hat":{"Color":"YELLOW"' in res.data