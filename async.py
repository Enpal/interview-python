from tasks import get_weather_forecast

result = get_weather_forecast.delay()
data = result.get(timeout=10)
print(data)
