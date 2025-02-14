import requests

class OpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    def __init__(self):
        None

    def get_forecast(self):
        response = requests.get(self.BASE_URL)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
