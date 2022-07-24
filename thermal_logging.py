#!/usr/bin/env python3
import datetime as datetime
import time
import logging

import agent_openweather as openweather
import agent_nest as nest
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
        r = temperature.Temperature('95132,us', datetime.datetime.now(), local_temp)
        r.save()


        credentials = {
            'project_id' : '88fd3306-59ed-44f4-9134-06d1dd43878c',
            'client_id' : '740269163638-jpthukkg54pab72dadun2q912f18d2d8.apps.googleusercontent.com',
            'client_secret' : '2_I685cVfbMVhJX25fcWNGJE',
            'refresh_token' : '1//068GkykWUrLIsCgYIARAAGAYSNwF-L9IrflJWrXoj2I7bhE2EI_xeAP-iwXe4rlMo_Dqk1Wn9_OMW2ufnO28KLwWgYVvzG5QVkhc'
        }

        n = nest.NestAgent(**credentials)
        if n.get_new_access_token():
            # use the new access token to get the devie list
            list = n.get_device_list()
            if list is not None:
                ambient = n.parse_Temp_from_dlist(list)
                r = temperature.Temperature('nest', datetime.datetime.now(), ambient)
                r.save()

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    t = ThermalLogging()
    t.startCollectTemp()
    # while True:
    #     t.startCollectTemp()
    #     # sleep 10 minutes.
    #     time.sleep(60*10)

    

