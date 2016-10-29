#!/usr/bin/env python
import pika
import json

""" Reading configuration file
assume a default configuratin, if able to read one, overwrite it.
"""

# default configuration send to local host, read config file to overwrite it.
config = {'target_host': 'localhost'}
with open('thermal_logging.json', 'r') as f:
    config = json.load(f)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(config['target_host'],
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='thermal')

sample = ['sensor1', 25]

message = json.JSONEncoder().encode(sample)
channel.basic_publish(exchange='',
                      routing_key='thermal',
                      body=message)
print("[x], send %s" % message)
connection.close()
