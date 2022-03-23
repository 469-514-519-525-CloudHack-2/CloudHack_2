#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import pika, sys, os
from dotenv import load_dotenv
import json
import time
app = Flask(__name__)
print("Consumer going to sleep...")
time.sleep(60)
print("Consumer strted...")

load_dotenv("./consumerID.env")


CONSUMER_ID = os.getenv("CONSUMER_ID")
CONSUMER_IP = os.getenv("CONSUMER_IP")
consumer_details  = {"name":CONSUMER_ID,"IP":CONSUMER_IP}


res = requests.post('http://producer:8888/new_ride_matching_consumer', json=consumer_details)
# main()
print(res)
# return jsonify({"message":"message sent to new_ride_matching_consumer"})

# CONSUMER_ID=""
# print(consumer_details)

queue_name = "consumer_queue_{}".format(CONSUMER_ID)
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
channel = connection.channel()
print(queue_name)
def main():
    channel.queue_declare(queue = queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(json.loads(body.decode())["time"])
        print("awoken")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, auto_ack = False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    print("sup")
    # app.run(host=CONSUMER_IP, port=5000, debug=True)
    main()
    print("sup_again")

    