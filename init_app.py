import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow    
    

from sqlalchemy import create_engine
from sqlalchemy import exc
import time
import config

import logging
import logging.handlers

#handler = logging.handlers.SysLogHandler(address = '/dev/log')
#handler.setFormatter(logging.Formatter('flask [%(levelname)s] %(message)s'))
print('APP_SETTING ->',eval(os.environ['APP_SETTINGS']).SQLALCHEMY_DATABASE_URI)

while 1:
    try:
        print(0)
        e = create_engine(eval(os.environ['APP_SETTINGS']).SQLALCHEMY_DATABASE_URI)
        print('1')
        e.execute('select 1')
    except exc.OperationalError:
        print('Waiting for database...')
        time.sleep(1)
    else:
        break

print('Connected!')
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.logger.addHandler(handler)
db = SQLAlchemy(app)
ma = Marshmallow(db)