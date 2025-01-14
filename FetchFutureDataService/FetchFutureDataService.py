import requests
import os
from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime as dt

app = Flask(__name__)
app.debug 
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

@app.route("/forecast",methods=['GET'])
def fetchFutureData():
    datetime = request.args.get('datetime')
    weatherData = fetch_weather_data(datetime)
    if weatherData:
        return jsonify(weatherData), 200
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500


def fetch_weather_data(datetime):
    try:
        # Requête vers l'API OpenWeather
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
        print(f"URL de la requête : {response.url}")
        print(f"Statut de la réponse : {response.status_code}")

        if response.status_code == 200:
            allData = response.json()  # Décodage JSON
            # Filtrer les données pour obtenir celles du jour demandé
            allData = allData['list']
            print(f"Nombre de données reçues : {len(allData)}")

            # Convertir la date en format 'datetime' pour une comparaison facile
            datetime_obj = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
            print(f"Date recherchée : {datetime_obj}")

            # Filtrer les données où 'dt_txt' correspond à la date et l'heure demandées
            filtered_data = [entry for entry in allData if dt.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S") == datetime_obj]
            
            if filtered_data:
                print(f"Données pour la date et l'heure demandées : {filtered_data}")
                return filtered_data
            else:
                print(f"Aucune donnée trouvée pour la date {datetime_obj}")
                return None
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
    