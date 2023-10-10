import json
import re
import redis

from mongoengine import connect

from models import Author, Quote
from connect import uri

# Connect to MongoDB
connect(host=uri)

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, password=None, decode_responses=True)


def search_by_tag(tag):
    tags_regex=re.compile(f"^{tag}", re.IGNORECASE)
    # Check if result is in cache
    cached_result = redis_client.get(f'tag:{tags_regex}')
    if cached_result:
        return json.loads(cached_result)
    
    quotes = Quote.objects(tags=tags_regex)
    result = [(quote.author.fullname, quote.quote) for quote in quotes]
    # Cache the result in Redis
    redis_client.set(f'tag:{tag}', json.dumps(result))
    return result


def search_by_tags(tags_search):
    # Check if result is in cache
    cached_result = redis_client.get(f'tags:{tags_search}')
    if cached_result:
        return json.loads(cached_result)
    quotes = Quote.objects(tags__in=tags_search)
    result = [(quote.author.fullname, quote.quote) for quote in quotes]
    redis_client.set(f'tags:{tags_search}', json.dumps(result))
    return result

def search_by_author(author_name):
    author_regex=re.compile(f"^{author_name}", re.IGNORECASE)
    cached_result = redis_client.get(f'tag:{author_regex}')
    if cached_result:
        return json.loads(cached_result)
    author = Author.objects(fullname=author_regex).first()
    if author:
        quotes = Quote.objects(author=author)
        result = [(quote.author.fullname, quote.quote) for quote in quotes]
        redis_client.set(f'tag:{author_regex}', json.dumps(result))
        return result
    else:
        return []


while True:

    instruction = "Give me the command. Ex.: 'name:Steve Martin' or 'tag:life' or 'tags:life,live'. Type 'exit' to exit"
    print(instruction)
    try:
        user_input_command = input(">>>").strip()

        if user_input_command == "exit":
            print("Program closed")
            break
        user_command = user_input_command.split(":")

        if len(user_command) != 2:
            print(instruction)
            continue

        command, value = user_command
        command = command.lower()

        if command == "name":
            quotes = search_by_author(value)
        elif command == "tag":
            quotes = search_by_tag(value)
        elif command == "tags":
            tags_search = value.split(",")
            quotes = search_by_tags(tags_search)
        else:
            print(instruction)
            continue

        if quotes:
            for author, quote in quotes:
                print(f"Author: {author}\nQuote: {quote}\n")
        else:
            print("No quotes.")
    except Exception as err:
        print(err)
