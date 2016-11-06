#!/usr/bin/env python
import pika
import json
import time

from ds18b20 import read_sensor

""" Reading configuration file
assume a default configuratin, if able to read one, overwrite it.
"""

# default configuration send to local host, read config file to overwrite it.
config = {'target_host': 'localhost'}
with open('thermal_logging.json', 'r') as f:
    config = json.load(f)
sensors = config['sensors']

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(config['target_host'],
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='thermal')

while True:
	data = dict()
	data['measurement'] = 'thermal'
	data_tags = dict()
	data_tags['sensor'] = sensors[0]
	data_fields = dict()
	data_fields['value'] = read_sensor(sensors[0])
	data['tags'] = data_tags
	data['fields'] = data_fields

	message = json.JSONEncoder().encode(data)
	channel.basic_publish(exchange='',
			      routing_key='thermal',
			      body=message)
	print("[x], send %s" % message)
	time.sleep(60)


connection.close()

