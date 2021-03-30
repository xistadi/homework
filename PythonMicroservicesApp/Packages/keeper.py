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
