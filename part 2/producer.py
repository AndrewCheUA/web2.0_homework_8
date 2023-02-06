import json
from random import randint
from datetime import datetime

import pika

from database.model import Contacts
import database.connect as connect
from connect_seed import generate_contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='task_exchange', exchange_type='direct')
channel.queue_declare(queue='email_task_queue', durable=True)
channel.queue_bind(exchange='task_exchange', queue='email_task_queue')

channel.queue_declare(queue='sms_task_queue', durable=True)
channel.queue_bind(exchange='task_exchange', queue='sms_task_queue')


if __name__ == '__main__':
    # generate_contacts(10)
    contacts= Contacts.objects()
    
    for contact in contacts:
        if contact.email_preferred == True:
            print(contact.id)
            c_id = str(contact.id)
            message = {
                'contact_id': c_id,
                'payload': f"Task result {randint(1, 500)}",
                'created_at': datetime.now().isoformat()
            }
            
            channel.basic_publish(
                exchange='task_exchange',
                routing_key='email_task_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            print(f"Send email message: {message}")
            
        if contact.email_preferred == False:
            print(contact.id)
            c_id = str(contact.id)
            message = {
                'contact_id': c_id,
                'payload': f"Task result {randint(1, 500)}",
                'created_at': datetime.now().isoformat()
            }
            
            channel.basic_publish(
                exchange='task_exchange',
                routing_key='sms_task_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            print(f"Send sms: {message}")
    
    connection.close()