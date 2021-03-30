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


def scrape_from_api():
    url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
    source = requests.get(url)
    all_rate = source.json()
    all_rate = [rate for rate in all_rate]
    system("cls||clear")
    print('Курс белорусского рубля\n' + '=' * 30)
    for rate in all_rate:
        for kek, kek2 in rate.items():
            if kek == 'Cur_Name':
                print(f'{kek2}: ', end='')
            elif kek == 'Cur_OfficialRate':
                print(f'{kek2} BLR')
    print('=' * 30)
    return all_rate


def insert_sql(all_rate):
    base = declarative_base()
    engine = create_engine('sqlite:///sqlalchemy_microservices_app.db')
    base.metadata.bind = engine
    dbsession = sessionmaker(bind=engine)
    session = dbsession()
    date = Dates()
    for rate in all_rate:
        for kek, kek2 in rate.items():
            if kek == 'Cur_Name':
                name_exrate = kek2
            elif kek == 'Cur_OfficialRate':
                amount_exrate = kek2
                exrate = ExchangeRates(name=name_exrate, amount=amount_exrate, date=date)
                session.add(exrate)
    session.commit()
