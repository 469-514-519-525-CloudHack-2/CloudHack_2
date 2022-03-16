#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import json
from random import randint

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='database_queue')


app = Flask(__name__)
consumers = []

@app.route("/")
def index():
	return jsonify({"message": "success"})

@app.route("/new_ride", methods = ["POST"])
def new_ride():
	data = request.json
	print(data)
	string_data = json.dumps(data)
	print(consumers, len(consumers))
	matched_ride_idx = randint(0, len(consumers) - 1)
	# print(matched_ride_idx, len(consumers))
	matched_ride = consumers[matched_ride_idx]["consumer_id"]
	queue_name = 'consumer_queue_{}'.format(matched_ride)
	channel.queue_declare(queue = queue_name)
	channel.basic_publish(exchange = '', routing_key = queue_name, body = string_data)
	print("Sent to {}".format(queue_name))
	# connection.close()
	return jsonify({"message": "success"})

@app.route("/new_ride_matching_consumer", methods = ["POST"])
def new_ride_matching_consumer():
	data = request.json
	consumers.append(data)
	print(consumers, len(consumers))
	return jsonify({"consumers":consumers})
    
	

if __name__ == '__main__':
    app.run(port=8888, debug=True)
