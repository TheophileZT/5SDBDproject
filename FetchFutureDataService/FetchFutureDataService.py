import requests 
import os
from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime as dt
import logging

# Initialiser le logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
port = int(os.environ.get('PORT', 5001))

# Paramètres de la requête
params = {
    'lat': 43.6,
    'lon': 1.44,
    'appid': "ad8f9db26c6726c4f963aaa047fbf875",  # Clé API
    'units': 'metric'
}

@app.route("/")
def home():
    logging.info("Accès au point d'entrée principal.")
    return "Hellඞ, this is a Flask Microservice FetchFutureDataService!"

@app.route("/forecast", methods=['GET'])
def fetchFutureData():
    datetime = request.args.get('datetime')
    logging.info(f"Requête reçue pour la date et l'heure : {datetime}")

    try:
        weatherData = fetch_weather_data(datetime)
        if not weatherData:
            logging.error("Échec de la récupération des données météorologiques.")
            return jsonify({"error": "Failed to fetch weather data"}), 500
        
        logging.debug(f"Données météo récupérées avec succès : {weatherData}")

        event_data = fetch_event_data(datetime)
        if not event_data:
            logging.error("Échec de la récupération des données d'événements.")
            return jsonify({"error": "Failed to fetch event data"}), 500

        body_event = event_data['results']
        
        station_info = requests.get("http://localhost:5002/score", json={"event": body_event})

        result = []
        for station in station_info.json():
            station_entry = {
                "number": station["number"],
                "station_name": station["station_name"],
                "cluster": station["cluster"],
                "lat": station["lat"],
                "lng": station["lng"],
                "counter_events": station["counter_events"],
                "percentage_cloud_coverage": weatherData["clouds"]["all"],
                "visibility_distance": weatherData["visibility"],
                "percentage_humidity": weatherData["main"]["humidity"],
                "current_temperature": weatherData["main"]["temp"],
                "feels_like_temperature": weatherData["main"]["feels_like"],
                "is_rainy": 1 if "rain" in weatherData else 0,
                "status":1
            }
            result.append(station_entry)

        logging.info("Données générées avec succès pour la réponse.")
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Erreur lors du traitement de la requête : {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


def fetch_event_data(datetime):
    date = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
    try:
        logging.info(f"Récupération des données d'événements pour {datetime}.")
        response = requests.get(
            f"https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/agenda-des-manifestations-culturelles-so-toulouse/records?where=date_debut<='{date.isoformat()}' AND date_fin>='{date.isoformat()}'"
        )
        logging.debug(f"Statut de la réponse des événements : {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"Erreur {response.status_code} lors de la récupération des données d'événements.")
            return None
    except Exception as e:
        logging.error(f"Une erreur est survenue lors de la récupération des données d'événements : {e}")
        return None


def fetch_weather_data(target_datetime):
    try:
        logging.info(f"Récupération des données météorologiques pour {target_datetime}.")
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
        logging.debug(f"URL de la requête : {response.url}")
        logging.debug(f"Statut de la réponse météo : {response.status_code}")

        if response.status_code == 200:
            allData = response.json()['list']
            target_datetime_obj = dt.strptime(target_datetime, "%Y-%m-%d %H:%M:%S")

            allData_with_datetime = [
                {
                    "dt": dt.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S"),
                    "data": entry
                }
                for entry in allData
            ]

            exact_match = next((entry['data'] for entry in allData_with_datetime if entry['dt'] == target_datetime_obj), None)
            if exact_match:
                logging.info("Correspondance exacte trouvée.")
                return exact_match

            allData_with_datetime.sort(key=lambda x: x['dt'])

            before = None
            after = None
            for entry in allData_with_datetime:
                if entry['dt'] <= target_datetime_obj:
                    before = entry
                elif entry['dt'] > target_datetime_obj and after is None:
                    after = entry
                    break

            if before and after:
                logging.info("Interpolation des données météorologiques.")
                return interpolate_weather_data(before['data'], after['data'], target_datetime_obj, before['dt'], after['dt'])
            elif before or after:
                return before['data'] if before else after['data']
            else:
                logging.warning("Aucune donnée météo trouvée.")
                return None
        else:
            logging.error(f"Erreur {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Une erreur est survenue lors de la récupération des données météo : {e}")
        return None


def interpolate_weather_data(before_data, after_data, target_datetime, before_datetime, after_datetime):
    total_diff = (after_datetime - before_datetime).total_seconds()
    elapsed_diff = (target_datetime - before_datetime).total_seconds()
    proportion = elapsed_diff / total_diff

    logging.debug(f"Proportion pour interpolation : {proportion}")

    interpolated_data = {}
    fields_to_interpolate = ['main', 'wind', 'clouds', 'visibility']
    for field in fields_to_interpolate:
        if field in before_data and field in after_data:
            if isinstance(before_data[field], dict):
                interpolated_data[field] = {
                    key: before_data[field][key] + proportion * (after_data[field][key] - before_data[field][key])
                    for key in before_data[field]
                }
            else:
                interpolated_data[field] = before_data[field] + proportion * (after_data[field] - before_data[field])

    interpolated_data['dt_txt'] = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return interpolated_data

if __name__ == "__main__":
    logging.info("Lancement de l'application Flask sur le port %d", port)
    app.run(host="0.0.0.0", port=port)
    