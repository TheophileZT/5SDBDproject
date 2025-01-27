from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import logging
import pandas as pd

app = Flask(__name__)
port = int(os.environ.get('PORT', 5003))
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

params = {
    'contract': 'Toulouse',
    'apiKey': "747abc58543245b99b316a08dece9b29bd42662d"
}

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice StationService!"

@app.route("/stations", methods=['GET'])
def get_stations():
    try:
        response = requests.get("https://api.jcdecaux.com/vls/v1/stations", params=params)
        response.raise_for_status()  # Ensure the request was successful
        logging.info("Stations fetched successfully.")
        return jsonify(response.json())  # Return JSON directly
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch stations: {e}")
        return jsonify({"error": "Failed to fetch stations"}), 500


@app.route("/stations/cluster", methods=['GET'])
def get_stations_with_cluster():
    try:
        response = requests.get("https://api.jcdecaux.com/vls/v1/stations", params=params)
        response.raise_for_status()  # Ensure the request was successful
        logging.info("Stations fetched successfully.")
        
        clusters = pd.read_csv("clustered_stations.csv")
        stations = response.json()
        
        for station in stations:
            station_id = station.get("number")
            cluster = clusters[clusters["station"] == station_id]
            if not cluster.empty:
                station["cluster"] = int(cluster["cluster"].values[0])
            station["lat"] = station["position"]["lat"]
            station["lng"] = station["position"]["lng"]
            station.pop("position")
            station["station_name"] = station["name"]
            station.pop("name")
        
        return jsonify(stations)
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch stations: {e}")
        return jsonify({"error": "Failed to fetch stations"}), 500
    except FileNotFoundError as e:
        logging.error(f"Cluster file not found: {e}")
        return jsonify({"error": "Cluster file not found"}), 500
    except pd.errors.EmptyDataError as e:
        logging.error(f"Cluster file is empty: {e}")
        return jsonify({"error": "Cluster file is empty"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/status", methods=['POST'])
def get_status():
    try:
        predictions = request.get_json()
        if not predictions:
            logging.error("No predictions received.")
            return jsonify({"error": "No predictions received"}), 400

        response = requests.get("https://api.jcdecaux.com/vls/v1/stations", params=params)
        response.raise_for_status()
        stations = response.json()
        logging.info("Stations fetched successfully for status computation.")

        # Map station data by number for quick lookup
        station_map = {station["number"]: station for station in stations}

        for prediction in predictions:
            station_number = prediction.get("number")
            if station_number not in station_map:
                logging.warning(f"Station number {station_number} not found in JCDecaux data.")
                continue

            station = station_map[station_number]
            prediction["station_name"] = station.get("name")
            position = station.get("position", {})
            prediction["lat"] = position.get("lat")
            prediction["lng"] = position.get("lng")

            bike_stands = station.get("bike_stands", 0)
            available_bikes = prediction.get("available_bikes", 0)

            if bike_stands > 0:
                ratio = available_bikes / bike_stands
                if ratio < 0.1:
                    status = "Critically Underloaded"
                elif ratio < 0.3:
                    status = "Underloaded"
                elif ratio < 0.7:
                    status = "Balanced"
                elif ratio < 0.9:
                    status = "Overloaded"
                else:
                    status = "Critically Overloaded"
            else:
                status = "No bike stands available"

            prediction["bike_stands"] = bike_stands
            prediction["status"] = status

        logging.info("Status computed successfully.")

        return jsonify(predictions), 200

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch status: {e}")
        return jsonify({"error": "Failed to fetch status"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
