#!/usr/bin/env python 
import pika
import subprocess
import shlex
from loguru import logger

command = 'rtl_433 -q -G -F json'

def main():
    logger.info("Message Send Queue Started")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
    except Exception as e:
        print("Error creating pika blocking connection: " + str(e))
        return("Failed")
    channel = connection.channel()
    channel.queue_declare(queue='rtl-433')

    try:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, encoding='utf8')
    except Exception as e:
        print("Error opening subprocess: " + str(e))
        connection.close()
        return("Failed")
      
    while True:
        output = process.stdout.readline()
        channel.basic_publish(exchange='',
            routing_key='rtl-433',
            body=output)

    connection.close()

if __name__ == '__main__':
    main()
