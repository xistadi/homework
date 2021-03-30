import requests
from os import system
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Packages.keeper import ExchangeRates, Dates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import flask
from flask import jsonify 


def input_api():
    Base = declarative_base()
    engine = create_engine('sqlite:///sqlalchemy_microservices_app.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    dict_for_api = {}
    query = session.query(Dates, ExchangeRates)
    query = query.join(Dates, Dates.id == ExchangeRates.date_id).order_by(Dates.date)
    records = query.all()
    for date, exrate in records:
        print(f'{date.date.strftime("%A, %d. %B %Y %I:%M%p")} - {exrate}')
        if date.date.strftime("%A, %d. %B %Y %I:%M%p") in dict_for_api:
            dict_for_api[date.date.strftime("%A, %d. %B %Y %I:%M%p")].update({exrate.name: exrate.amount})
        else:
            dict_for_api[date.date.strftime("%A, %d. %B %Y %I:%M%p")] = {exrate.name: exrate.amount}
    dict_for_api = dict_for_api[list(dict_for_api)[-1]]

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return jsonify(dict_for_api)
    app.run()
