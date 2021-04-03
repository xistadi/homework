import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import flask
from flask import jsonify, request


Base = declarative_base()
engine = create_engine('sqlite:///sqlalchemy_microservices_app.db?check_same_thread=False')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
dbsession = sessionmaker(bind=engine)
session = dbsession()


class ExchangeRates(Base):
    """Class exchange rates (id, name, amount)"""
    __tablename__ = 'exrates'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    amount = Column(Float, nullable=False)
    date_id = Column(Integer, ForeignKey('dates.id'))
    date = relationship("Dates", back_populates="exrates")

    def __str__(self):
        return self.name


class Dates(Base):
    """Class dates (id, date)"""
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exrates = relationship("ExchangeRates", back_populates="date")

    def __str__(self):
        return self.date


class Keeper:
    """Class keeper"""

    def __init__(self):
        self.all_rate = {}
        self.dict_for_api = {}

    def get_data_from_reaper(self):
        """Get all_rate json from reaper"""
        url = 'http://reaper:3300'
        source = requests.get(url)
        self.all_rate = source.json()

    def insert_sql(self):
        """Insert new information into db from reaper"""
        Base.metadata.create_all(engine)
        date = Dates()
        for rate in self.all_rate:
            for key, value in rate.items():
                if key == 'Cur_Name':  # if key == name exchange rate
                    name_exrate = value
                elif key == 'Cur_OfficialRate':  # if key == amount exchange rate
                    amount_exrate = value
                    exrate = ExchangeRates(name=name_exrate, amount=amount_exrate, date=date)  # create new ExchangeRates in db
                    session.add(exrate)
        session.commit()

    def input_api(self):
        """Input api from keeper localhost port 3200"""
        query = session.query(Dates, ExchangeRates)  # query to get Dates and ExchangeRates
        query = query.join(Dates, Dates.id == ExchangeRates.date_id).order_by(Dates.date)
        records = query.all()
        for date, exrate in records:
            if date.date.strftime("%A, %d. %B %Y %I:%M%p") in self.dict_for_api:  # if date already exist
                self.dict_for_api[date.date.strftime("%A, %d. %B %Y %I:%M%p")].update({exrate.name: exrate.amount})  # update dict new values
            else:  # if date is new
                self.dict_for_api[date.date.strftime("%A, %d. %B %Y %I:%M%p")] = {exrate.name: exrate.amount}  # input new values with date
        self.dict_for_api = self.dict_for_api[list(self.dict_for_api)[-1]]  # get the last one

        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        @app.route('/', methods=['POST', 'GET'])
        def home():
            if request.method == 'POST':
                a = Keeper()
                a.get_data_from_reaper()
                a.insert_sql()
                return flask.redirect('http://localhost:3100')
            else:
                return jsonify(self.dict_for_api)
        app.run(host='0.0.0.0', port=3200)


if __name__ == "__main__":
    a = Keeper()
    a.get_data_from_reaper()
    a.insert_sql()
    a.input_api()
