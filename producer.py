from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route("/new_ride", methods = ["POST"])
def new_ride():
	data = request.json


@app.route("/new_ride_matching_consumer", methods = ["POST"])
def new_ride_matching_consumer():
	data = request.json
    
	

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
