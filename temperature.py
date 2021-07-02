#!/usr/bin/env python3

import sqlalchemy as db
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime


import database as database

Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'Temp'

    sensor = Column(db.Text(255), nullable=False, index=True)
    datetime = Column(Integer, primary_key=True)
    temp = Column(db.Float())


    def __init__(self, sensor, datetime, temp):
        self.sensor = sensor
        self.datetime = datetime
        self.temp = temp    
        self.db = database.Database()

    def save(self):
        self.db.getSession().add(self)
        self.db.getSession().commit()


    def __repr__(self):
        return "<Temp {}, loc={}, at {}>".format(self.temp, self.sensor, self.datetime)

if __name__ == '__main__':
    t = Temperature('95132,us', datetime.datetime.now(), 24.0)
    t.save()
