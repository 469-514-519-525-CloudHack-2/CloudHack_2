#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__, template_folder='.')

seqNo = 1

@app.route("/")
def index():
	return jsonify({"message":"consumer master set up success"})

@app.route("/get_consumerID")
def get_consumerID():
    count = len(open('./consumerID.env').readlines())
    global seqNo
    d = {}
    if((2*(seqNo-1) + 1) >= count):
        d = {"seqNo": -1} # Out of consumer IDs
    else:
        temp = seqNo
        seqNo = seqNo + 1
        d = {"seqNo": temp}
    return jsonify(d)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8989, debug=True)
