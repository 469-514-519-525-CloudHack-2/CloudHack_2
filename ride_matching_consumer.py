#!/usr/bin/env python
import pika, sys, os
from dotenv import load_dotenv
import json
import time
print("Consumer going to sleep...")
time.sleep(30)
print("Consumer strted...")

load_dotenv("./consumerID.env")

# CONSUMER_ID = os.getenv("CONSUMER_ID")
CONSUMER_ID="test"
queue_name = "consumer_queue_{}".format(CONSUMER_ID)
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
channel = connection.channel()
print(queue_name)
def main():
    channel.queue_declare(queue = queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(json.loads(body.decode())["time"])
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
