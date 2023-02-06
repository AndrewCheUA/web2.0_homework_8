import re

import redis
from redis_lru import RedisLRU

from database.models import Quotes, Authors
import database.connect as connect


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def name_search(author):
    quotes = Quotes.objects()
    authors = Authors.objects(fullname=author.strip())
    quotes_tag = []
    for author in authors:
        quotes = Quotes.objects(author=author.id)
        for quote in quotes:
            quotes_tag.append(quote.quote)
    return quotes_tag


@cache
def tag_search(s_result):
    quotes = Quotes.objects()
    tag_counter = len(s_result)
    quotes_tag = []
    while tag_counter > 1:
        for quote in quotes:
            if s_result[tag_counter-1].strip() in quote.tags:
                quotes_tag.append(quote.quote)
                tag_counter = tag_counter - 1
    return quotes_tag
    

if __name__ == '__main__':
    search = True
    
    while search:
        user_input = input("Please enter your input: ")
        s_result =re.split(':|,', user_input)
        if len(s_result) == 2 and s_result[0] == "name":
            author_name = s_result[1].strip()
            print(name_search(author_name))
            
        elif 2 < len(s_result[0]) < 5 and s_result[0].startswith("tag"):
            print(tag_search(s_result))
        
        elif s_result[0] == "exit":
            search = False
            print("Bye!")
            
        else:
            print("Incorrect input.")
    
    