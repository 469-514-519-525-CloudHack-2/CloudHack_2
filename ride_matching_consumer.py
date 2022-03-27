#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import pika, sys, os
from dotenv import load_dotenv
import json
import time
print("Consumer going to sleep...")
time.sleep(10)
print("Consumer coming back from sleep...")

app = Flask(__name__)

load_dotenv("./consumerID.env")
load_dotenv("./producerID.env")

res = requests.get("http://consumer_master:8989/get_consumerID").json()
if(res["seqNo"] == -1):
    print("Maximum Consumer Limit reached. Exiting gracefully.")
    exit(0)

CONSUMER_ID = os.getenv("CONSUMER_ID"+str(res["seqNo"]))
CONSUMER_IP = os.getenv("CONSUMER_IP"+str(res["seqNo"]))
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
        print("Received {} in consumer {}".format(body.decode(), CONSUMER_ID))
        print("Consumer "+CONSUMER_ID+" Busy")
        try:
            time.sleep(int(json.loads(body.decode())["time"]))
        except:
            print("Cannot Sleep")
        print("Consumer "+CONSUMER_ID+" Back")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(queue_name, callback, auto_ack = False)

    print('Waiting for messages in the consumer '+CONSUMER_ID+' queue')
    channel.start_consuming()

if __name__ == '__main__':
    main()

    