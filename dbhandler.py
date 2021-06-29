#!/usr/bin/env python3
import sqlalchemy as db
from sqlalchemy import table, column, insert
from sqlalchemy.sql.sqltypes import DateTime


class DbHandler:
    DB='temperature.sqlite'
    table = table('Temp',
                        column('sensor'),
                        column('datetime'),
                        column('temp')
    )

    def save(self, **kwargs):
        conn  = self.getConn()
        query = insert(DbHandler.table).values(**kwargs) 
        ResultProxy = conn.execute(query)

    def getConn(self):
        if self.conn is None:
            engine = db.create_engine("sqlite:///{}".format(DbHandler.DB)) #Create test.sqlite automatically
            conn = engine.connect()

            # create table
            metadata = db.MetaData()

            emp = db.Table('Temp', metadata,
                        db.Column('sensor', db.Text(255), nullable=False),
                        db.Column('datetime', db.DateTime),
                        db.Column('temp', db.Float(), default=100.0)
                        )

            metadata.create_all(engine) #Creates the table
            self.conn = conn
        return self.conn


    def __init__(self):
        self.conn = None