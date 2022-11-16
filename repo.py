from redis import Redis
import os
import logging
from dotenv import load_dotenv
load_dotenv()

# connection = Redis(db=1)
connection = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),
                password=os.getenv('REDIS_PASSWORD'), db=os.getenv('REDIS_DB'), decode_responses=True)

to_visit_key = 'crawling:to_visit'
visited_key = 'crawling:visited'
queued_key = 'crawling:queued'
content_key = 'crawling:content'
proxy_key = 'proxies:valid'

# To Visit
def add_to_visit(value):
    # LPOS command is not available in Redis library
    # TO-DO: Error handling
    if connection.execute_command('LPOS', to_visit_key, value) is None:
        # add URL to the end of the list
        connection.rpush(to_visit_key, value)

def pop_to_visit_blocking(timeout=0):
    logging.info('Pop to visit blocking.')
    # pop URL from the beginning of the list
    # TO-DO: Error handling
    return connection.blpop(to_visit_key, timeout)
    
# Visited
def count_visited():
    logging.info('Count as visited.')
    # TO-DO: Error handling
    return connection.scard(visited_key)

def add_visited(value):
    # TO-DO: Error handling
    connection.sadd(visited_key, value)

def is_visited(value):
    # TO-DO: Error handling
    return connection.sismember(visited_key, value)

# Queued
def count_queued():
    logging.info('Count as queued.')
    # TO-DO: Error handling
    return connection.scard(queued_key)

def add_to_queue(value):
    # TO-DO: Error handling
    connection.sadd(queued_key, value)

def is_queued(value):
    # TO-DO: Error handling
    return connection.sismember(queued_key, value)

def move_from_queued_to_visited(value):
    # atomically move a URL from queued to visited
    # TO-DO: Error handling
    connection.smove(queued_key, visited_key, value)

# Content
def set_content(key, value):
    # TO-DO: Error handling
    connection.hmset(content_key, key=key, value=value)

def add_to_list(list, value):
    # TO-DO: Error handling
    connection.rpush(list, value)

# Proxies
def add_to_valid_proxies(ip):
    # if connection.execute_command('LPOS', proxy_key, ip) is None:
    #     # add URL to the end of the list
    #     connection.rpush(to_visit_key, ip)
    #     return
    connection.rpush(proxy_key, ip)

def clear_proxies():
    connection.delete(proxy_key)
    
def get_valid_proxies_list():
    valid_proxies = connection.lrange(proxy_key, 0, -1)
    print(valid_proxies)
    return valid_proxies