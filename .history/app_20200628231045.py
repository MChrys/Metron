import os 

from flask import Flask, jsonify






def create_app(config=None):
    app = Flask(__name__)


    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    @app.route('/add/<table>')
    def add(table):
        if table == 'Character':
            pass
        elif table == 'Hat':
            pass
        else:
            raise KeyError("This Table doesn't exist") 

    @app.route('/update/<table>/<idx>')
    def update(table , idx):
        if table == 'Character':
            #id 
            pass
        elif table == 'Hat':
            pass
        else:
            raise KeyError("This Table doesn't exist") 