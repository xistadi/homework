import requests
from os import system
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import flask
from flask import jsonify 


Base = declarative_base()


class ExchangeRates(Base):
    # класс пользователей (id, name, amount)
    __tablename__ = 'exrates'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    amount = Column(Float, nullable=False)
    date_id = Column(Integer, ForeignKey('dates.id'))
    date = relationship("Dates", back_populates="exrates")

    def __str__(self):
        return self.name


class Dates(Base):
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exrates = relationship("ExchangeRates", back_populates="date")

    def __str__(self):
        return self.date


engine = create_engine('sqlite:///sqlalchemy_microservices_app.db')
Base.metadata.create_all(engine)

def get_data_from_reaper():
    url = 'http://reaper:3300'
    source = requests.get(url)
    all_rate = source.json()
    #print(f'==========\n{all_rate}')
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
    print(records)
    for date, exrate in records:
        #print(f'{date.date.strftime("%A, %d. %B %Y %I:%M%p")} - {exrate}')
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
    app.run(host='0.0.0.0', port=3200)


if __name__ == "__main__":
    all_rate = get_data_from_reaper()
    insert_sql(all_rate)
    input_api()
