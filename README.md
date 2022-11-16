# Enpal Python task

This repository is the base work for a live coding interview at Enpal.

## Installing dependencies

`pip install -r requirements.txt`

## Running the application synchronously

`python main.py`

## Running tests

`python -m unittest tests/forecast.py`

## (Optionally) running the appliction asynchronously

`docker run -p 6379:6379 redis`

On Mac / Linux:

```
celery -A tasks worker --loglevel=INFO
python async.py
```

on Windows:

```pip install gevent
celery -A tasks worker --loglevel=INFO -P gevent
python async.py```
