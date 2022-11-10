# Entry point for Celery
from celery import Celery
from crawler import crawl, add_results_to_queue
from parserList import get_parser
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

queue_name = 'celery'
 
app = Celery('tasks', broker_url=os.getenv('BROKER_URL')) 

app_client = app.connection().channel().client

logging.info("Celery connected.")
 
@app.task
async def queue_url(url, maximum_items):
    logging.info("Queue URL starting.")
    # Celery's queue length
    queued_count = app_client.llen(queue_name)

    # get the parser, either custom or the default one
    parser = get_parser(url)
    logging.info(f"Parser: {parser.get_html}.")
    result = await crawl(url, queued_count, maximum_items,
                   parser.get_html, parser.extract_content)

    logging.info(f"Result: {result}")

    if result is None:
        logging.info("No Result returned.")
        return 'Failed to return result.'

    content = result

    logging.info(f"Final content returned: {content}")
    
    # parser.store_content(url, content)

    return content
