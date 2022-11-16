from entsoe import EntsoePandasClient
import pandas as pd
import requests
from delorean import parse

cities = {
    "Madrid": {
        "lat": 40.4167,
        "long": -3.7033,
    },
    "Barcelona": {
        "lat": 41.346176,
        "long": 2.168365,
    },
    "Bilbao": {
        "lat": 	43.262985,
        "long": -2.935013,
    },
    "Malaga": {
        "lat": 36.719444,
        "long": -4.420000,
    }
}

# already ran ahead of time, result in data/forecast.csv
def prepare_forecast():
    client = EntsoePandasClient(api_key="API_KEY")

    start = pd.Timestamp('20221010', tz='Europe/Brussels')
    end = pd.Timestamp('20221011', tz='Europe/Brussels')
    country_code = 'ES'

    ts = client.query_wind_and_solar_forecast(country_code, start=start, end=end)
    ts.to_csv('data/forecast.csv')

def get_weather_forecast():
    r = requests.get(f"https://archive-api.open-meteo.com/v1/era5?latitude={cities['Madrid']['latitude']}&longitude={cities['Madrid']['longitude']}&start_date=2022-10-09&end_date=2022-10-11&hourly=temperature_2m,windspeed_10m")
    data = r.json()
    return data

def enhance_generation_forecast(forecast):
    ts = pd.read_csv('data/forecast.csv', index_col=0)
    ts['temperature'] = None
    ts['windspeed'] = None

    for i, hour in enumerate(forecast['hourly']['time']):
        # TODO there seems to be a subtle bug here regarding https://delorean.readthedocs.io/en/latest/quickstart.html#ambiguous-cases
        date = parse(hour, timezone=forecast['timezone_abbreviation'])
        date = date.shift("Europe/Madrid")
        key = date.datetime.strftime("%Y-%m-%d %H:%M:%S%z")
        key = key[:-2] + ':' + key[-2:]
        if key in ts.index:
            ts.loc[[key], ['temperature']] = forecast['hourly']['temperature_2m'][i]

            #  TODO for good forecast of wind generation we should take the wind speed at 100m instead, turbines are way taller than 10m.
            ts.loc[[key], ['windspeed']] = forecast['hourly']['windspeed_10m'][i]

    ts = ts.fillna(method='pad')    
    ts.to_csv('data/result.csv')


if __name__ == '__main__':
    forecast = get_weather_forecast()
    enhance_generation_forecast(forecast)
