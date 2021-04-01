import requests
from os import system
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import flask
from flask import jsonify 

def get_data_from_keeper():
    url = 'http://keeper:3200'
    source = requests.get(url)
    dict_for_api = source.json()
    print(f'==========\n{dict_for_api}')
    return dict_for_api

def input_api(dict_for_api):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return jsonify(dict_for_api)
    app.run(host='0.0.0.0', port=3100)

if __name__ == "__main__":
    dict_for_api = get_data_from_keeper()
    input_api(dict_for_api)
