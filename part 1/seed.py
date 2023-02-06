import json

from database.models import Quotes, Authors
import database.connect as connect


with open("authors.json", 'r', encoding='utf-8') as authors:
    authors_data = json.load(authors)

with open('quotes.json', 'r', encoding='utf-8') as quotes:
    quotes_data = json.load(quotes)


for el in authors_data:
    record = Authors(fullname=el['fullname'],
                     born_date=el['born_date'],
                     born_location=el['born_location'],
                     description=el['description'])
    record.save()


for item in quotes_data:
    authors = Authors.objects(fullname=item['author'])
    for author in authors:
        record = Quotes(tags=item['tags'],
                        author=author.id,
                        quote=item['quote'])
        record.save()