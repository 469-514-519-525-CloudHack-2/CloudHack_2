from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import json
import requests
import pika, sys, os
import json
import time

# app = Flask(__name__)

queue_name = "database_queue"
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
channel = connection.channel()

def addData():
    host=MongoClient("mongodb://mongoDB")

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        res = body.decode()
        print(" [x] Received %r" % res)
        # time.sleep(json.loads(body.decode())["time"])
        print("awoken")
        ch.basic_ack(delivery_tag = method.delivery_tag)
        db=host["consumerDB"]
        collection=db["consumers"]
        sample_data=json.loads(res)
        print("Sample data",sample_data)
        collection.insert_one(sample_data)

        var = list(collection.find())
        print('Inserted into the MongoDB database!')  
        print("Objects in Database:",var)
        # return 'JSON added'

    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, auto_ack = False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    # return "Received at database"
    


if __name__ == '__main__':
    addData()
#     app.run(host="0.0.0.0", port=5001, debug=True)
#     print("App stopped Listening...")