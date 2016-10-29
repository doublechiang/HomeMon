#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='thermal')


def callback(ch, method, properties, body):
    record = json.loads(body)
    print(" [x] Received %r" % repr(record))

channel.basic_consume(callback,
                      queue='thermal',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
