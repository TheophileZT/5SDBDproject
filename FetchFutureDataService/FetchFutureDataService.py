import requests
import os
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)
port = int(os.environ.get('PORT', 5001))

# Paramètres de la requête
params = {
    'lat':43.6,
    'lon':1.44,
    'appid': "ad8f9db26c6726c4f963aaa047fbf875",  # Clé API
}

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice FetchFutureDataService!"

@app.route("/forecast")
def fetchFutureData():
    weatherData = fetch_weather_data()
    if weatherData:
        return jsonify(weatherData), 200
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500


def fetch_weather_data():
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
        if response.status_code == 200:
            allData = response.json()  
            return allData
        else:
            print(f"Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
    