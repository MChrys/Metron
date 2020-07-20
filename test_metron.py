

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
 
    # Establish an application context before running the tests
    ctx = test_app.app_context()
    ctx.push()
 
    yield testing_client  
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    #db = SQLAlchemy()
    # Create the database and the database table

    db.create_all()

    # Insert user data
    data = {'Name' :'Dog','Age':5, 'Weight':60,'Human':False,'Hat': None}
  
    
    character_schema = CharacterSchema()
    chara1 = Character(**data)

    db.session.add(chara1)

    # Commit the changes for the users
    db.session.commit()

    yield db  
    db.session.close()
    db.drop_all()




def test_index(test_client, init_database):
    res =test_client.get("/index")
    assert res.status_code == 200
    assert b"hello Metron" in res.data


def test_create(test_client,init_database):
    res = test_client.post("/create?Name=Alain&Age=18&Weight=80&Human=True&Color=YELLOW")
    assert res.status_code == 200
    assert b'Age":18' in res.data
    assert b'"Human":true' in res.data
    assert b'"Name":"Alain","Weight":80' in res.data
    assert b'"Hat":{"Color":"YELLOW"' in res.data


def test_delete(test_client, init_database):
    res = test_client.get("/read_all")
    
    import json
    characters = json.loads(res.data.decode("utf-8").replace('\n',''))
    liste = characters['characters']
    lenght = len(liste)
    idx = str(int(liste[-1]['Id']))

    res2 = test_client.get("/delete/{}".format(idx))
    assert res.status_code ==202
    

def test_update(test_client, init_database):
    res = test_client.get("/read_all")

    import json
    characters = json.loads(res.data.decode("utf-8").replace('\n',''))
    liste = characters['characters']
    lenght = len(liste)
    idx = str(int(liste[-1]['Id']))
    res2 = test_client.get("/read/{}".format(idx))
    character = json.loads(res2.data.decode("utf-8").replace('\n',''))
    print(character)
    color = bytes(character['character']['Hat']['Color'],'utf-8')
    assert color in res2.data
    res3 = test_client.put("/update/{}?Color=GREEN".format(idx))
    res4 = test_client.get("/read/{}".format(idx))
    assert b'GREEN' in res4.data
