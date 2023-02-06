import json
from random import randint
from datetime import datetime

import pika

from database.model import Contacts
import database.connect as connect
from connect_seed import generate_contacts




contacts= Contacts.objects()

for contact in contacts:
    x = str(contact.id)
    print(contact.id)
    contact.update(message_sent=False)