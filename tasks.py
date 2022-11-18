from celery import Celery
from parsers import defaults
from crawler import crawl
import os
import logging
from dotenv import load_dotenv
load_dotenv()

queue_name = 'celery'
 
app = Celery('tasks', broker_url=os.getenv('BROKER_URL')) 

app_client = app.connection().channel().client

logging.info("Celery connected.")
 
@app.task()
async def queue_url(url):
    # TO-DO: Error handling
    logging.info("Queue URL starting.")
    queued_count = app_client.llen(queue_name)

    logging.info(f"Celery's queue count: {queued_count}")

    parser = defaults
    logging.info(f"Parser: {parser.get_html}.")
    result = await crawl(url, parser.get_html, parser.extract_content)

    logging.info(f"Result: {result}")

    if result is None:
        logging.info("No Result returned.")
        return 'Failed to return result.'

    content = result

    logging.info(f"Final content returned: {content}")
    
    # parser.store_content(url, content)

    return content
