#!/usr/bin/env python
import pika, sys, os
from dotenv import load_dotenv

load_dotenv("./consumerID.env")

CONSUMER_ID = os.getenv("CONSUMER_ID")
queue_name = "consumer_queue_{}".format(CONSUMER_ID)
print(queue_name)
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = queue_name)

    def callback(ch, method, properties, body):
        print("Received {}".format(body))

    channel.basic_consume(queue_name, callback, auto_ack = True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
