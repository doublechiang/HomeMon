#!/usr/bin/env python3
import sqlalchemy as db
from sqlalchemy import table, column, insert
from sqlalchemy.sql.sqltypes import DateTime
import datetime
import time


import weather

class ThermalLogging:
    """ Main program to handle house thermal logging.
        Colect data, save to Influx database.
    """
    DB='temperature.sqlite'
    table = table('Temp',
                        column('sensor'),
                        column('datetime'),
                        column('temp')
    )

    def startCollectTemp(self):
        w = weather.Weather('95132,us')
        local_temp = w.getCurrentTemp()
        record = {
            'sensor': "95132,us",
            'datetime': datetime.datetime.now(),
            'temp': local_temp
        }
        self.__save(**record)

    
    def __save(self, **kwargs):
        conn  = self.__getDbConn()
        query = insert(ThermalLogging.table).values(**kwargs) 
        ResultProxy = conn.execute(query)


    def __getDbConn(self):
        if self.conn is None:
            engine = db.create_engine("sqlite:///{}".format(ThermalLogging.DB)) #Create test.sqlite automatically
            self.conn = engine.connect()

            # create table
            metadata = db.MetaData()

            emp = db.Table('Temp', metadata,
                        db.Column('sensor', db.Text(255), nullable=False),
                        db.Column('datetime', db.DateTime),
                        db.Column('temp', db.Float(), default=100.0)
                        )

            metadata.create_all(engine) #Creates the table
        return self.conn
    def __init__(self):
        self.conn = None

if __name__ == '__main__':
    t = ThermalLogging()
    while True:
        t.startCollectTemp()
        # sleep 1 hours
        time.sleep(60*60)

    

