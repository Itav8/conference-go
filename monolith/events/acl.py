import requests
from events.keys import OPEN_WEATHER_API_KEY


def get_weather_data(city, state):
    # Create the URL for the geocoding API with the city and state
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }

    r = requests.get(url, params=params)
    content = r.json()

    try:
        lat = content[0]["lat"]
        lon = content[0]["lon"]
    except (KeyError, IndexError):
        return None

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    url = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.get(url, params=params)
    content = r.json()
    return {
        "description": content["weather"][0]["description"],
        "temp": content["main"]["temp"],
    }
