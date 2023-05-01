import pika
import random
import hashlib
import sys, os
import json


def demine_mine(ch, method, properties, body):
    serial_num = json.loads(body.decode('utf-8'))['serial_number']

    # print(body)
    print(f'Beginning to demine {serial_num}')

    # sets random pin and preforms hashing function,
    # copied from lab 1
    pin = random.randint(1, 99999999999)
    tempKey = str(pin) + serial_num
    hash = hashlib.sha256(tempKey.encode()).hexdigest()

    while (not str(hash).startswith("000")):
        pin = random.randint(1, 99999999999)
        tempKey = str(pin) + serial_num
        hash = hashlib.sha256(tempKey.encode()).hexdigest()
    # print the various keys and serial numbers and hash values hashed
    # from the above code
    print("Serial Number: " + serial_num)
    print("Temporary Key: " + tempKey)
    print("Hash Value: " + str(hash))
    print("pin:" + str(pin))


    # send message to defused queue
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='defused-queue')

    body = {
        'serial_num': serial_num,
        'pin': pin,
    }
    bodyString = json.dumps(body).encode('utf-8')

    channel.basic_publish(exchange='', routing_key='defused-queue', body=bodyString)
    connection.close()


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='demine-queue')

    channel.basic_consume(queue='demine-queue', on_message_callback=demine_mine, auto_ack=True)

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
