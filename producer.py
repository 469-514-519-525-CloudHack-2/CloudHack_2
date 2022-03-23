#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from random import randint
import time
print("Producer going to sleep...")
time.sleep(5)
print("Producer Woken back up...")

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
	# data = request.json
	data = {}
	data["dst"] = request.form.get("dst")
	data["pickup"] = request.form.get("pickup")
	data["time"] = request.form.get("time")
	data["seats"] = request.form.get("seats")
	data["cost"] = request.form.get("cost")
	print(data)
	string_data = json.dumps(data)
	# print(consumers, len(consumers))
	matched_ride_idx = randint(0, len(consumers) - 1)
	# print(matched_ride_idx, len(consumers))
	matched_ride = consumers[matched_ride_idx]["name"]
	# matched_ride = "test"
	queue_name = 'consumer_queue_{}'.format(matched_ride)
	channel.queue_declare(queue = queue_name)
	channel.basic_publish(exchange = '', routing_key = queue_name, body = string_data)
	print("Sent to {}".format(queue_name))
	# connection.close()
	return redirect("/")

@app.route("/new_ride_matching_consumer", methods = ["POST"])
def new_ride_matching_consumer():
	data = request.json
	consumers.append(data)
	print(consumers, len(consumers))
	return jsonify({"consumers":consumers})
    
	

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)
