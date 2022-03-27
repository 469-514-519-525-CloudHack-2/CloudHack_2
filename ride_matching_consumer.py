#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import pika, sys, os
from dotenv import load_dotenv
import json
import time
print("Consumer going back to sleep...")
time.sleep(20)
print("Consumer coming back up...")
app = Flask(__name__)

load_dotenv("./consumerID.env")
load_dotenv("./producerID.env")


CONSUMER_ID = os.getenv("CONSUMER_ID")
CONSUMER_IP = os.getenv("CONSUMER_IP")
PRODUCER_IP = os.getenv("PRODUCER_IP")
PRODUCER_PORT = os.getenv("PRODUCER_PORT")

consumer_details  = {"name":CONSUMER_ID,"IP":CONSUMER_IP}

url = 'http://'+PRODUCER_IP+':'+PRODUCER_PORT+'/new_ride_matching_consumer'
res = requests.post(url, json=consumer_details)

queue_name = "consumer_queue_{}".format(CONSUMER_ID)
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
channel = connection.channel()

def main():
    channel.queue_declare(queue = queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        print("Consumer Busy!")
        try:
            time.sleep(int(json.loads(body.decode())["time"]))
        except:
            print("Cannot Sleep")
        print("Consumer Back!")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(queue_name, callback, auto_ack = False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    # app.run(host=CONSUMER_IP, port=5000, debug=True)
    main()

    