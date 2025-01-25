from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError, MeanSquaredError

from datetime import datetime as dt
import requests
import logging
import os

# Initialiser le logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

# Charger le scaler et le modèle
try:
    scalers_x = {
        0: load("scaler_X_cluster0.pkl"),
        1: load("scaler_X_cluster1.pkl"),
        2: load("scaler_X_cluster2.pkl"),
        3: load("scaler_X_cluster3.pkl"),
    }
    logging.info("Scalers chargés avec succès.")
    models = {0: load_model(
                "cnn_model_for_cluster0.h5",
                custom_objects={
                    "mse": MeanSquaredError(),
                    "mae": MeanAbsoluteError()}),
            2:load_model(
                "cnn_model_for_cluster2.h5",
                custom_objects={
                    "mse": MeanSquaredError(),
                    "mae": MeanAbsoluteError()})
    }
    logging.info("Modèles chargés avec succès.")
except FileNotFoundError as e:
    logging.error(f"Erreur lors du chargement du modèle ou du scaler : {e}")
    exit(1)

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice Inference!"

@app.route("/predict", methods=['GET'])
def inference():
    datetime_str = request.args.get('datetime')
    if not datetime_str:
        return jsonify({"error": "Missing 'datetime' parameter"}), 400

    try:
        data = get_features(datetime_str)
    except Exception as e:
        logging.error(f"Erreur dans la fonction get_features : {e}")
        return jsonify({"error": str(e)}), 500

    try:
        # Préparer les données comme à l'entraînement
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['timestamp_numeric'] = data['timestamp'].view(np.int64) // 10**9
        data['day_of_week'] = data['timestamp'].dt.dayofweek

        data = data.drop(columns=['timestamp', 'is_rainy'])

        standardScale_feature = [
            'status', 'visibility_distance', 'current_temperature',
            'feels_like_temperature', 'wind_speed', 'counter_events',
            'timestamp_numeric', 'day_of_week'
        ]

        predictions = []
        grouped = data.groupby('cluster')

        for cluster, group in grouped:
            if cluster == 1 or cluster == 3:
                continue
            group = group.drop(columns='cluster')

            scaler_x = scalers_x[cluster]
            model = models[cluster]
            group[standardScale_feature] = scaler_x.transform(group[standardScale_feature])
            group_reshaped = group.to_numpy().reshape((group.shape[0], 1, group.shape[1]))

            cluster_predictions = np.round(model.predict(group_reshaped)).astype(int)
            for number, prediction in zip(group['number'], cluster_predictions):
                predictions.append({
                    'cluster': cluster,
                    'number': number,
                    'available_bikes': int(prediction[0])
                })

        logging.info("Prédictions effectuées avec succès.")
        return jsonify(predictions)

    except Exception as e:
        logging.error(f"Erreur lors de la prédiction : {e}")
        return jsonify({"error": str(e)}), 500


def get_features(str_datetime):
    try:
        response = requests.get("http://localhost:5001/forecast?datetime=" + str_datetime)
        response.raise_for_status()
        logging.info("Données externes récupérées avec succès.")
        external_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la récupération des données externes : {e}")
        raise Exception("Failed to fetch external data")

    try:
        target_datetime = dt.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
        hour = target_datetime.hour
        day_of_week = target_datetime.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        logging.debug(f"Informations temporelles : hour={hour}, day_of_week={day_of_week}, is_weekend={is_weekend}")
    except ValueError as e:
        logging.error(f"Erreur de parsing du datetime : {e}")
        raise ValueError("Invalid datetime format, expected 'YYYY-MM-DD HH:MM:SS'")

    data = []
    for station in external_data:
        data.append({
            "timestamp": target_datetime,
            "number": station["number"],
            "status": station["status"],
            "bikes_stand": station["bike_stands"],
            "visibility_distance": station["visibility_distance"],
            "current_temperature": station["current_temperature"],
            "feels_like_temperature": station["feels_like_temperature"],
            "is_rainy": station["is_rainy"],
            "wind_speed": station["wind_speed"],
            "counter_events": station["counter_events"],
            "cluster": station["cluster"]
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
