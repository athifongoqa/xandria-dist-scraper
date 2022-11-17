# Entry point to start queuing URLs
from tasks import queue_url 
import repo
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from headers import allowed_headers
from proxies.cron import free_proxies
import logging
import validators
import os
os.system("playwright install")

def create_app() -> FastAPI:
    logging.basicConfig(level=logging.DEBUG)

    logging.info('App created.')

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["POST"],
        allow_headers=allowed_headers,
    )
    
    app.add_middleware(HTTPSRedirectMiddleware)

    @app.get("/proxies")
    async def cronJob():
        free_proxies()
        return 'Done'

    @app.post("/")
    async def startProcess(req: Request):
        # TO-DO: Error handling
        processed = await req.json()
        starting_url = processed['url']

        if not validators.url(starting_url, public=True):
            logging.info(f'Not a valid URL: {starting_url}')
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Bad request.")

        logging.info(f'Starting: {starting_url}')
        
        repo.add_to_visit(starting_url)

        try:
            while True:
                next = repo.pop_to_visit_blocking(2)
                logging.info(f"next received: {next}")
                if next is None:
                    logging.info('Timeout! No more items to process')
                    break
                url = next[1]
                logging.info(f"URL received: {url}")
                payload = await queue_url(url)
                return JSONResponse(status_code=status.HTTP_200_OK, content=payload)
        except:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content='Issue processing request. Try again.')

    return app