from flask import Flask, jsonify, request
import requests
import os
import logging
import joblib
from datetime import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import pandas as pd

# Initialiser le logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

# Charger le scaler et le modèle
try:
    scaler = joblib.load("scaler_X.pkl")
    logging.info("Scaler chargé avec succès.")
    scalerY = joblib.load("scaler_y.pkl")
    
    model = tf.keras.models.load_model('cnn_model.h5')
    logging.info("Modèle chargé avec succès.")
except FileNotFoundError as e:
    logging.error(f"Erreur lors du chargement du modèle ou du scaler : {e}")
    exit(1)

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice Inference!"

@app.route("/predict", methods=['GET'])
def inference():
    datetime_str  = request.args.get('datetime')
    logging.info(f"Requête reçue pour la date et l'heure : {datetime_str}")

    # Récupérer les données externes
    try:
        response = requests.get("http://localhost:5001/forecast", params={"datetime": datetime_str})
        response.raise_for_status()  # Vérifie si la réponse a un statut 200
        logging.info("Données externes récupérées avec succès.")
        external_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la récupération des données externes : {e}")
        return jsonify({"error": "Failed to fetch external data"}), 500

    # Extraire les informations temporelles
    try:
        target_datetime = dt.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        hour = target_datetime.hour
        day_of_week = target_datetime.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        logging.debug(f"Informations temporelles : hour={hour}, day_of_week={day_of_week}, is_weekend={is_weekend}")
    except ValueError as e:
        logging.error(f"Erreur de parsing du datetime : {e}")
        return jsonify({"error": "Invalid datetime format, expected 'YYYY-MM-DD HH:MM:SS'"}), 400

    

    try:
        # Extraire les caractéristiques nécessaires
        features_list = []
        stations = []

        for data in external_data:
            feature = [
                data["number"],
                data["status"],
                data["percentage_cloud_coverage"],   
                data["visibility_distance"],
                data["percentage_humidity"],
                data["current_temperature"],
                data["feels_like_temperature"],
                data["is_rainy"],
                hour,
                day_of_week,
                is_weekend
            ]
            features_list.append(feature)
            stations.append(data["number"])

        features_df = pd.DataFrame(features_list, columns=[
            'number', 'status', 'percentage_cloud_coverage',
            'visibility_distance', 'percentage_humidity', 'current_temperature',
            'feels_like_temperature', 'is_rainy', 'hour', 'day_of_week', 'is_weekend'
        ])

        # Transformer les données avec le scaler
        features_scaled = scaler.transform(features_df)
        features_scaled = features_scaled.reshape(features_scaled.shape[0], 1, features_scaled.shape[1])

    except KeyError as e:
        logging.error(f"Données manquantes ou incorrectes : {e}")
        return jsonify({"error": f"Missing or invalid data: {e}"}), 400
    except Exception as e:
        logging.error(f"Erreur lors de la préparation des données : {e}")
        return jsonify({"error": "Error while preparing data"}), 500

    try:
        predictions = model.predict(features_scaled)
        y_pred  = scalerY.inverse_transform(predictions)
        response = []
        for station, bikes in zip(stations, y_pred.flatten()):
            response.append({
                'station': station,
                'available_bikes': round(float(bikes), 2)
            })

        response_clean = requests.post("http://localhost:5003/status", json=response)

        response_clean.raise_for_status()
        logging.info("Inference effectuée avec succès.")
        return jsonify(response_clean.json())
    except Exception as e:
        logging.error(f"Erreur lors de l'inférence : {e}")
        return jsonify({"error": "Error during inference"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
    