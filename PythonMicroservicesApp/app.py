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

engine = create_engine('sqlite:///sqlalchemy_microservices_app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

date = Dates()
session.add(date)
session.commit()

exrate = ExchangeRates(name='Тенге', amount=6.1807, date=date)
session.add(exrate)
session.commit()


"""for rate in all_rate:
    for kek, kek2 in rate.items():
        if kek == 'Cur_Name':
            name_exrate = kek2
        elif kek == 'Cur_OfficialRate':
            amount_exrate = kek2
            exrate = ExchangeRates(name=name_exrate, amount=amount_exrate, date=date)
            session.add(exrate)
    session.commit()"""
dict_test = {}
query = session.query(Dates, ExchangeRates)
query = query.join(Dates, Dates.id == ExchangeRates.date_id).order_by(Dates.date)
records = query.all()
for date, exrate in records:
    dict_test[date.date.strftime("%A, %d. %B %Y %I:%M%p")] = exrate.name, exrate.amount
print(dict_test)
"""
for date, exrate in records:
    print(f'{date.date}\t{exrate.name}\t\t\t{exrate.amount}')
    """


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():

    return jsonify(dict_test)

app.run()