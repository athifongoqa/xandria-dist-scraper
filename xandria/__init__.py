# Entry point to start queuing URLs
from tasks import queue_url 
import repo
from fastapi import FastAPI, Request

def create_app() -> FastAPI:
    app = FastAPI()

    maximum_items = 30

    @app.post("/")
    async def startProcess(req: Request):
        starting_url = await req.body()
        repo.add_to_visit(starting_url)

        while True:
            total = repo.count_visited() + repo.count_queued()
            if total >= maximum_items:
                print('Exiting! Over maximum:', total)
                break

            # timeout after 1 minute
            item = repo.pop_to_visit_blocking(60)
            if item is None:
                print('Timeout! No more items to process')
                break

            url = item[1].decode('utf-8')
            print('Pop URL', url)
            queue_url.delay(url, maximum_items)

        return "Done"

    return app