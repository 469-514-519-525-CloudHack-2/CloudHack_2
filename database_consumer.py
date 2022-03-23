from crypt import methods
from matplotlib import collections
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/addData',methods=['POST'])
def addData():
    host=MongoClient("172.17.0.2")
    channel = connection.channel()
    channel.queue_declare(queue='database_queue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback, queue='database_queue', no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    db=host["consumerDB"]
    collection=db["consumers"]
    sample_data=request.json
    collection.insert_one(sample_data)
    print('Inserted into the MongoDB database!')  
    return 'JSON added'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
    print("App stopped Listening...")