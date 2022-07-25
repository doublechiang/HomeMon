#!/usr/bin/env python3
import os
import psycopg2
import sqlalchemy as db
from sqlalchemy import table, column, insert
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import sessionmaker

import temperature

class Database:
    _instance = None
    _session = None
    _conn = None
    _engine = None

    # DB='sqlite:///temperature.sqlite'
    DB='postgresql+psycopg2://homemon:homemon@localhost/homemon'

    def __new__(cls):
        if cls._instance is None:

            cls._instance = super(Database, cls).__new__(cls)
            # put any new init code here
            db_url = os.environ['DATABASE_URL']
            if db_url is None:
                db_url = Database.DB
            engine = db.create_engine(db_url) #Create test.sqlite automatically
            cls._engine = engine
            conn = engine.connect()
            
            # create table
            metadata = db.MetaData()

            emp = db.Table('Temp', metadata,
                        db.Column('sensor', db.String(32), nullable=False),
                        db.Column('datetime', db.DateTime, primary_key=True),
                        db.Column('temp', db.Float(), default=100.0)
                        )
            metadata.create_all(engine) #Creates the table
            
            cls._conn = conn
            Session = sessionmaker(bind=engine)
            cls._session = Session()

        return cls._instance

    def getSession(self):
        return Database._session

    @DeprecationWarning
    def save(self, **kwargs):
        conn  = self.getConn()
        query = insert(DbHandler.table).values(**kwargs) 
        ResultProxy = conn.execute(query)

    def getConn(self):
        return Database._conn

    def getEngine(self):
        return Database._engine

    def __init__(self):
        pass


if __name__ == '__main__':
    a = Database()
    print (a.getSession())
    b = Database()
    print(b.getSession())
