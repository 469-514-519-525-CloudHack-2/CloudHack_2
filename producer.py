#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from random import randint
import time
from dotenv import load_dotenv
import os
print("Producer going to sleep...")
time.sleep(10)
print("Producer Woken back up...")

load_dotenv("./producerID.env")

PRODUCER_IP = os.getenv("PRODUCER_IP")
PRODUCER_PORT = os.getenv("PRODUCER_PORT")

import pika

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://rabbitmq?connection_attempts=5&retry_delay=5'))

channel = connection.channel()

channel.queue_declare(queue='database_queue')


app = Flask(__name__, template_folder='.')
consumers = []

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/new_ride", methods = ["POST"])
def new_ride():
	data = {}
	data["dst"] = request.form.get("dst")
	data["pickup"] = request.form.get("pickup")
	data["time"] = request.form.get("time")
	data["seats"] = request.form.get("seats")
	data["cost"] = request.form.get("cost")
	string_data = json.dumps(data)
	matched_ride_idx = randint(0, len(consumers) - 1)
	matched_ride = consumers[matched_ride_idx]["name"]
	queue_name = 'consumer_queue_{}'.format(matched_ride)
	channel.queue_declare(queue = queue_name)
	channel.basic_publish(exchange = '', routing_key = queue_name, body = string_data)
	channel.basic_publish(exchange = '', routing_key = 'database_queue', body = string_data)
	print("Sent to {}".format(queue_name))
	return redirect("/")

@app.route("/new_ride_matching_consumer", methods = ["POST"])
def new_ride_matching_consumer():
	data = request.json
	consumers.append(data)
	print(consumers, len(consumers))
	return jsonify({"consumers":consumers})
    
	

if __name__ == '__main__':
    app.run(host=PRODUCER_IP, port=PRODUCER_PORT, debug=True)
