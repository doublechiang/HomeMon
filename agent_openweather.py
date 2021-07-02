import requests
import json
import os
import logging

class OpenWeather:
    """ Agent to get area temperature from OpenWeather API
    """
    WEATHER_APPKEY = 'WEATHER_APPKEY'
    API = 'http://api.openweathermap.org/data/2.5/weather'
    
    def __init__(self, loc):
        self.loc = loc

    def getCurrentTemp(self, loc=None):
        """ Get Current Temperature, if something wrong, return None.
        """
        temp = None
        if loc is None:
            loc=self.loc

        # We get the 
        key = os.getenv(OpenWeather.WEATHER_APPKEY)
        if key is None:
            logging.error('WEATHER_APPKEY is not defined in environment variable.')
        else:
            params={'zip': loc,
                'appid': key,
                'units': 'metric'}
            r =requests.get(OpenWeather.API, params=params)
            if r.status_code == 200:
                data=json.loads(r.text)
                temp = data['main']['temp']

        return temp            


if __name__ == "__main__":
    r = OpenWeather('95132,us')
    print(r.getCurrentTemp())