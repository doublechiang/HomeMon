#!/usr/bin/env python
import pika
import json
from influxdb import InfluxDBClient

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.50'))
channel = connection.channel()

channel.queue_declare(queue='thermal')


def callback(ch, method, properties, body):
    record = json.loads(body)
    print(" [x] Received %r" % repr(record))
    points = list()
    points = [record]
    client.write_points(points)


channel.basic_consume(callback,
                      queue='thermal',
                      no_ack=True)

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'thermal')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
