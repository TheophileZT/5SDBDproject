import requests, json, logging
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def convert_wind_speed_to_kmh(speed_mps):
    return speed_mps * 3.6

def process_weather_data(response, city):
    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
    wind_speed = convert_wind_speed_to_kmh(response['wind']['speed'])
    wind_deg = response.get('wind', {}).get('deg', None)
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    visibility = response['visibility']
    cloud_coverage = response['clouds']['all']
    rain_last_hour = response.get('rain', {}).get('1h', 0.0)
    snow_last_hour = response.get('snow', {}).get('1h', 0.0)
    description = response['weather'][0]['description']
    sunrise_time = datetime.fromtimestamp(response['sys']['sunrise'])
    sunset_time = datetime.fromtimestamp(response['sys']['sunset'])
    current_time = datetime.fromtimestamp(response['dt'])
    temp_min_celsius = kelvin_to_celsius(response['main']['temp_min'])
    temp_max_celsius = kelvin_to_celsius(response['main']['temp_max'])

    return {
        "timestamp": datetime.now(timezone.utc),
        "city": city,
        "latest_update_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "description": description,
        "temperature": {
            "current": round(temp_celsius, 2),
            "feels_like": round(feels_like_celsius, 2),
            "min": round(temp_min_celsius, 2),
            "max": round(temp_max_celsius, 2),
            "unit": "°C"
        },
        "pressure": {"current": pressure, "unit": "hPa"},
        "wind": {"speed": round(wind_speed, 2), "direction_degrees": wind_deg, "unit": "km/h"},
        "humidity": {"value": humidity, "unit": "%"},
        "visibility": {"distance": visibility, "unit": "m"},
        "cloud_coverage": {"percentage": cloud_coverage, "unit": "%"},
        "precipitation": {
            "rain_last_hour": {"value": rain_last_hour, "unit": "mm"},
            "snow_last_hour": {"value": snow_last_hour, "unit": "mm"}
        },
        "local_times": {
            "sunrise": sunrise_time.strftime("%Y-%m-%d %H:%M:%S"),
            "sunset": sunset_time.strftime("%Y-%m-%d %H:%M:%S"),
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logger.error("Configuration file not found.")
    raise

API_KEY = config["villes"][0]["weather_api_url"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
URI = config["dbInfos"]["uri"]
CITY = config["villes"][0]["nom"]
URL = f"{BASE_URL}appid={API_KEY}&q={CITY}"

response = requests.get(URL).json()

if response['cod'] != 200:
    logger.error(f"API error: {response['cod']}")
    raise Exception("Failed to fetch weather data.")

response_data = response
weather_data = process_weather_data(response_data, CITY)

try:
    client = MongoClient(URI, server_api=ServerApi('1'))
    db = client[config["dbInfos"]["dbName"]]
    client.admin.command('ping')
    logger.info("Connected to MongoDB!")
    collection = db[config["dbInfos"]["collectionName"]]
    collection.insert_one(weather_data)
    logger.info("Weather data inserted successfully.")
except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise
finally:
    client.close()
    logger.info("Disconnected from MongoDB.")
