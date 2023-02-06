import random

from faker import Faker

from database.model import Contacts
import database.connect as connect


def generate_contacts(num):
    fake = Faker()

    for contact in range(num):
        record = Contacts(fullname = fake.name(),
                        phone = fake.phone_number(),
                        email = fake.email(),
                        email_preferred = bool(random.getrandbits(1)),
                        message_sent = False)
        record.save()
        
        
if __name__ == '__main__':
    generate_contacts()