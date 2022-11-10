# Xandria Distributed Scraper

## Installation
You will need [Redis](https://redis.io/) and [python3 installed](https://www.python.org/downloads/). After that, install all the necessary libraries by running `pip3 install`.

```bash
pip3 install requests beautifulsoup4 playwright "celery[redis]"
```

## Execute

Configure the Redis connection in the [repo file](./repo.py) and Celery in the [tasks file](./tasks.py).

You need to start Celery... 

```bash
celery -A tasks worker
```

... and the run the web application.

```bash
uvicorn main:app --reload
```
