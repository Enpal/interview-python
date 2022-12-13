from celery import Celery
from main import prepare_forecast as prepare_forecast_sync, get_weather_forecast as get_weather_forecast_sync

BROKER_AND_BACKEND = "rabbitmq"

if BROKER_AND_BACKEND == "rabbitmq":
    BROKER_URL = 'amqp://guest:guest@localhost:5672'
    BACKEND_URL = 'rpc://guest:guest@localhost:5672'

else:
    # redis
    BROKER_URL = 'redis://localhost:6379/0'
    BACKEND_URL = 'redis://localhost:6379/1'

app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

@app.task
def prepare_forecast():
    prepare_forecast_sync()

@app.task
def get_weather_forecast():
    get_weather_forecast_sync()
