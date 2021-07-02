#!/usr/bin/env python3
import sqlalchemy as db
from sqlalchemy import table, column, insert
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import sessionmaker

import temperature

class Database:
    _instance = None
    _session = None
    _conn = None

    DB='temperature.sqlite'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # put any new init code here
            engine = db.create_engine("sqlite:///{}".format(Database.DB)) #Create test.sqlite automatically
            conn = engine.connect()

            # create table
            metadata = db.MetaData()

            emp = db.Table('Temp', metadata,
                        db.Column('sensor', db.Text(255), nullable=False),
                        db.Column('datetime', db.DateTime, primary_key=True),
                        db.Column('temp', db.Float(), default=100.0)
                        )
            metadata.create_all(engine) #Creates the table
            temperature.Temperature.create(engine)
            
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

    def __init__(self):
        pass


if __name__ == '__main__':
    a = Database()
    print (a.getSession())
    b = Database()
    print(b.getSession())
