import math
import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import requests

# Initialiser le logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
port = int(os.environ.get('PORT', 5002))
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    logging.info("Accès au point d'entrée principal.")
    return "Hello, this is a Flask Microservice EventImpactScoringSystem!"

@app.route("/score", methods=['GET'])
def score():
    logging.info("Requête reçue sur le point /score.")
    body = request.get_json()

    if not body or "event" not in body:
        logging.warning("Requête invalide : clé 'event' manquante dans le corps JSON.")
        return jsonify({"error": "Invalid input: 'event' key is required in JSON body"}), 400
    
    
    stationsres = requests.get("http://station:5003/stations/cluster")

    if stationsres.status_code != 200:
        logging.error(f"Erreur lors de la récupération des stations : {stationsres.text}")
        return jsonify({"error": "Failed to fetch stations"}), 500
    
    stations = stationsres.json()
        
    events = body.get("event")
    event_with_closest_stations = []

    for event in events:
        event_lat = event.get("googlemap_latitude")
        event_lng = event.get("googlemap_longitude")

        if event_lat is None or event_lng is None:
            logging.warning(f"Événement ignoré en raison de coordonnées manquantes : {event}")
            continue

        closest_stations = get_closest_stations(stations, event_lat, event_lng)
        logging.debug(f"Stations les plus proches pour l'événement {event.get('identifiant')}: {closest_stations}")

        event_entry = {
            "id_event": str(event.get("identifiant")),
            "date_debut": event.get("date_debut"),
            "date_fin": event.get("date_fin"),
            "event_lat": event_lat,
            "event_lng": event_lng,
            "closest_stations": closest_stations,
        }
        event_with_closest_stations.append(event_entry)

    station_with_events = []
    for station in stations:
        nbEvents = 0
        for event in event_with_closest_stations:
            if station["number"] in event["closest_stations"]:
                nbEvents += 1

        station_entry = {
            "number": station["number"],
            "station_name": station["station_name"],
            "lat": station["lat"],
            "lng": station["lng"],
            "bike_stands": station["bike_stands"],
            "cluster": station["cluster"],
            "counter_events": nbEvents
        }
        station_with_events.append(station_entry)

    logging.info("Calcul des scores des stations terminé avec succès.")
    return jsonify(station_with_events), 200


def get_closest_stations(stations, event_lat, event_lng, max_distance=0.5):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Rayon moyen de la Terre en kilomètres
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    closest_stations = []

    for station in stations:
        station_lat = station["lat"]
        station_lng = station["lng"]
        distance = haversine(event_lat, event_lng, station_lat, station_lng)

        if distance <= max_distance:
            closest_stations.append(station.get("number"))

    logging.debug(f"Stations à une distance <= {max_distance} km de ({event_lat}, {event_lng}) : {closest_stations}")
    return closest_stations


if __name__ == "__main__":
    logging.info("Lancement de l'application Flask sur le port %d", port)
    app.run(host="0.0.0.0", port=port)
