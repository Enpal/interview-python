import unittest
from main import get_weather_forecast
import requests_mock

class TestForecastMethods(unittest.TestCase):
    @requests_mock.Mocker()
    def test_method_called(self, mock):
        mock.get('https://archive-api.open-meteo.com/v1/era5?latitude=40.4167&longitude=-3.7033&start_date=2022-10-09&end_date=2022-10-11&hourly=temperature_2m,windspeed_10m',
            json={"latitude":40.5,"longitude":-3.75,"timezone_abbreviation":"GMT","hourly":{"time":["2022-10-10T00:00","2022-10-10T01:00"],"temperature_2m":[14.6,14.3],"windspeed_10m":[7.1,5.4]}})
        data = get_weather_forecast()
        history = mock.request_history
        self.assertEqual(len(history), 1, "Should have been called once")
        self.assertEqual(len(data['hourly']['temperature_2m']), 2, "Should have two temperature measurements")

if __name__ == '__main__':
    unittest.main()