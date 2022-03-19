#!/usr/bin/env python
from sqlite3 import connect
import pika, sys, os
from dotenv import load_dotenv
import json
import time

load_dotenv("./consumerID.env")

CONSUMER_ID = os.getenv("CONSUMER_ID")
queue_name = "consumer_queue_{}".format(CONSUMER_ID)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
print(queue_name)
def main():
    channel.queue_declare(queue = queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(json.loads(body.decode())["time"])
        print("awoken")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, auto_ack = False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
