#!/usr/bin/env python3

from google.oauth2 import service_account
import requests
import logging
import json

# curl -L -X POST 'https://www.googleapis.com/oauth2/v4/token?client_id=740269163638-jpthukkg54pab72dadun2q912f18d2d8.apps.googleusercontent.com&client_secret=2_I685cVfbMVhJX25fcWNGJE&code=4/0AX4XfWg7c2tWtdKnEFnarXxrUlJJOOzbGAWhO-47rhd75G8buMyqPa927nl-ZhQraZsrQw&grant_type=authorization_code&redirect_uri=https://www.google.com'

# {
#   "access_token": "ya29.a0ARrdaM8fydF82Zz4FY3UgHVlokR1qPVV4UqXgVA-rNqNFNviBZv_BUyy23RA2F0EItUHWNo3JIqw5ih7wo7ioNkLJvPDmWDAywdK8mrkzQZsohgH0CvUlk00FNnJIL5vgrYAQ7Qo-VO_tCrSW20fjICquJyN",
#   "expires_in": 3599,
#   "refresh_token": "1//0eQkelEO8pRZsCgYIARAAGA4SNwF-L9IrzNE76R-t3pn3eLy14UBY-85spny7h8GVEqf3E1idE7lF6sOMmWiTKNlYIt6F3sWK9zc",
#   "scope": "https://www.googleapis.com/auth/sdm.service",
#   "token_type": "Bearer"
# }

# DeviceID: AVPHwEv67PZLJ6CcIFf6veOBoDHDEE3Ay7eZmquceaTx-z75B1tYivmKIEch1Vh-SoVe1XFzTs8qHYBCACH_HJ4ZjRcPNQ

class NestAgent:
    DEVICE_LIST_API="https://smartdevicemanagement.googleapis.com/v1/enterprises/{}/devices"
    def get_device_list(self):
        """ Get the Device List Json string.
            return None if something wrong.
        """

        auth_str = "Bearer {}".format(self.get_access_token())
        headers= { 'Content-Type': 'application/json', 
            'Authorization': auth_str }

        url = NestAgent.DEVICE_LIST_API.format(self.project_id)
        r = requests.get(url, headers=headers)
        logging.info(r.text)
        if r.status_code == 200:
            return r.text
        return None

    def parse_Temp_from_dlist(self, data):
        dlist= json.loads(data)
        d = dlist.get('devices')[0]
        traits = d.get('traits')
        temp = traits.get('sdm.devices.traits.Temperature')
        ambient = temp.get('ambientTemperatureCelsius')
        if ambient is not None:
            return float(ambient)
        return None

    def get_new_access_token(self):
        # do not have access token, renew it.4
        url = 'https://www.googleapis.com/oauth2/v4/token'
        params = {
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'refresh_token' : self.refresh_token,
            'grant_type' : 'refresh_token'
        }
        r =requests.post(url, params=params)
        logging.info("get new token: {}".format(r.text))
        if r.status_code == 200:
            ret = json.loads(r.text)
            self.access_token = ret.get('access_token')
            return True
        return False

    def get_access_token(self):
        if self.access_token is None:
            self.access_token = self.refresh_token()

        return self.access_token

    def __init__(self, **kwargs):
        # assign the dict into instance variable
        for key, value in kwargs.items():
            cmd = "self.{}='{}'".format(key, value)
            exec(cmd)
        self.access_token = None

if __name__ == '__main__':
    credentials = {
        'project_id' : '88fd3306-59ed-44f4-9134-06d1dd43878c',
        'client_id' : '740269163638-jpthukkg54pab72dadun2q912f18d2d8.apps.googleusercontent.com',
        'client_secret' : '2_I685cVfbMVhJX25fcWNGJE',
        'refresh_token' : '1//0eQkelEO8pRZsCgYIARAAGA4SNwF-L9IrzNE76R-t3pn3eLy14UBY-85spny7h8GVEqf3E1idE7lF6sOMmWiTKNlYIt6F3sWK9zc'
    }
    n = NestAgent(**credentials)
    if n.get_new_access_token():
        # use the new access token to get the devie list
        list = n.get_device_list()
        if list is not None:
            ambient = n.parse_Temp_from_dlist(list)
            print(ambient)


