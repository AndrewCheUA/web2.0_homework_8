import json
from time import sleep

import pika

from database.model import Contacts
import database.connect as connect


contacts= Contacts.objects()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='email_task_queue', durable=True)


def callback_result(ch, method, properties, body):
    message = json.loads(body)
    contact = Contacts.objects(id=message.get('contact_id'))
    for c in contact:
        print(c.fullname)
        c.update(message_sent=True)
    print(f"Received email message: {message}")
    sleep(2)
    print("Done!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

 
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_task_queue', on_message_callback=callback_result)
channel.start_consuming()
