# Entry point to start queuing URLs
from tasks import queue_url 
import repo
from fastapi import FastAPI, Request
import logging

def create_app() -> FastAPI:
    logging.info('App created.')

    app = FastAPI()

    maximum_items = 30

    @app.post("/")
    async def startProcess(req: Request):
        processed = await req.json()
        starting_url = processed['url']
        logging.info(f'start: {starting_url}')
        
        repo.add_to_visit(starting_url)

        while True:
            total = repo.count_visited() + repo.count_queued()
            logging.info(f'Total: {total}')
            if total >= maximum_items:
                logging.info(f'Over maximum: {total}')
                break

            # timeout after 2 seconds
            item = repo.pop_to_visit_blocking(2)
            logging.info(f"Item received: {item}")
            if item is None:
                logging.info('Timeout! No more items to process')
                break

            url = item[1].decode('utf-8')
            logging.info(f"URL received: {url}")
            print('Pop URL', url)
            final = await queue_url(url, maximum_items)

        return final

    return app