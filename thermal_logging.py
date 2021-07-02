#!/usr/bin/env python3
import datetime as datetime
import time
import logging

import agent_openweather as openweather
# import agent_nest as nest
import temperature

class ThermalLogging:
    """ Main Daemon to continue collect temperature and save to database
    """

    def startCollectTemp(self):
        loc = '95132,us'
        w = openweather.OpenWeather(loc)
        local_temp = w.getCurrentTemp()
        logging.info("{} get temperature {}".format(loc, local_temp))  
        # r = Temperature(loc, datetime.datetime.now(), local_temp)
        r = temperature.Temperature('95132,us', datetime.datetime.now(), 24.0)
        print (r)
        r.save()

if __name__ == '__main__':
    t = ThermalLogging()
    while True:
        t.startCollectTemp()
        # sleep 10 minutes.
        time.sleep(60*10)

    

