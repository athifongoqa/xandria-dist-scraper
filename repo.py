from redis import Redis
from dotenv import load_dotenv
import os
import logging
load_dotenv()

# connection = Redis(db=1)
connection = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),
                password=os.getenv('REDIS_PASSWORD'), db=os.getenv('REDIS_DB'))

to_visit_key = 'crawling:to_visit'
visited_key = 'crawling:visited'
queued_key = 'crawling:queued'
content_key = 'crawling:content'

# To Visit
def add_to_visit(value):
    # LPOS command is not available in Redis library
    if connection.execute_command('LPOS', to_visit_key, value) is None:
        # add URL to the end of the list
        connection.rpush(to_visit_key, value)

def pop_to_visit_blocking(timeout=0):
    logging.info('Pop to visit blocking.')
    # pop URL from the beginning of the list
    return connection.blpop(to_visit_key, timeout)

# Visited
def count_visited():
    logging.info('Count as visited.')
    return connection.scard(visited_key)

def add_visited(value):
    connection.sadd(visited_key, value)

def is_visited(value):
    return connection.sismember(visited_key, value)

# Queued
def count_queued():
    logging.info('Count as queued.')
    return connection.scard(queued_key)

def add_to_queue(value):
    connection.sadd(queued_key, value)

def is_queued(value):
    return connection.sismember(queued_key, value)


def move_from_queued_to_visited(value):
    # atomically move a URL from queued to visited
    connection.smove(queued_key, visited_key, value)

# Content
def set_content(key, value):
    connection.hset(content_key, key=key, value=value)

def add_to_list(list, value):
    connection.rpush(list, value)