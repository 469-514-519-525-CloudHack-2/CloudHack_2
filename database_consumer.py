from crypt import methods
from matplotlib import collections
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/addData',methods=['POST'])
def addData():
    host=MongoClient("172.17.0.2")  #docker inspect 
    # host=MongoClient("mongodb")
    db=host["consumerDB"]
    collection=db["consumers"]
    sample_data=request.json
    collection.insert_one(sample_data)
    print('Inserted into the MongoDB database!')
    # rec_data = collection.find_one({"name":"hello"})
    # print("Fecthed from MongoDB: ",rec_data)    
    return 'JSON added'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
    print("App started Listening...")