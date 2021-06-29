#!/usr/bin/env python3
import sqlalchemy as db
import datetime
import time
import dbhandler


import weather

class ThermalLogging:
    """ Main program to handle house thermal logging.
        Colect data, save to sqlite database
    """

    def startCollectTemp(self, loc):
        w = weather.Weather(loc)
        local_temp = w.getCurrentTemp()
        print("{} get temperature {}".format(loc, local_temp))  
        record = {
            'sensor': loc,
            'datetime': datetime.datetime.now(),
            'temp': local_temp
        }
        dbhandler.DbHandler().save(**record)

    

if __name__ == '__main__':
    t = ThermalLogging()
    while True:
        t.startCollectTemp('95132,us')
        # sleep 10 minutes.
        time.sleep(60*10)

    

