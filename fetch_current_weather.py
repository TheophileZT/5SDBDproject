import requests
from datetime import datetime

API_KEY = "MY_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
city = "Toulouse"
url = BASE_URL + "appid=" + API_KEY + "&q=" + city

response = requests.get(url).json()

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

def convert_wind_speed_to_kmh(speed_mps):
    speed_kph = speed_mps*3.6
    return speed_kph

temp_kelvin = response['main']['temp']
temp_celsius = kelvin_to_celsius(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
wind_speed = convert_wind_speed_to_kmh(response['wind']['speed'])
humidity = response['main']['humidity']
visibility = response['visibility']
cloud_coverage = response['clouds']['all']
rain_last_hour = response.get('rain', {}).get('1h', 0.0) 
snow_last_hour = response.get('snow', {}).get('1h', 0.0) 
description = response['weather'][0]['description']
sunrise_time = datetime.fromtimestamp(response['sys']['sunrise'])
sunset_time = datetime.fromtimestamp(response['sys']['sunset'])
current_time = datetime.fromtimestamp(response['dt'])

print(f"Weather information for {city}: ")
print(f"Latest update: {current_time}")
print(f"Description: {description}")
print(f"Temperature: {temp_celsius:.2f}°C, feels like: {feels_like_celsius:.2f}°C")
print(f"Wind speed: {wind_speed:.2f}km/h")
print(f"Humidity: {humidity}%")
print(f"Visibility: {visibility}m")
print(f"Cloud coverage: {cloud_coverage}%")
print(f"Rain in the last hour: {rain_last_hour}mm")
print(f"Snow in the last hour: {snow_last_hour}mm")
print(f"Sun rises at {sunrise_time} and sets at {sunset_time}")
