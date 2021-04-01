import requests
from os import system
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import flask
from flask import jsonify 


def scrape_from_api():
    url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
    source = requests.get(url)
    all_rate = source.json()
    all_rate = [rate for rate in all_rate]
    #system("cls||clear")
    print('Курс белорусского рубля\n' + '=' * 30)
    for rate in all_rate:
        for kek, kek2 in rate.items():
            if kek == 'Cur_Name':
                print(f'{kek2}: ', end='')
            elif kek == 'Cur_OfficialRate':
                print(f'{kek2} BLR')
    print('=' * 30)


    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return jsonify(all_rate)
    app.run(host='0.0.0.0', port=3300)


if __name__ == "__main__":
    scrape_from_api()
