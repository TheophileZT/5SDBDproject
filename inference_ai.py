from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import joblib

app = Flask(__name__)

# Load the saved CNN model and scalers
MODEL_PATH = 'cnn_model.h5'
SCALER_X_PATH = 'scaler_X.pkl'
SCALER_Y_PATH = 'scaler_y.pkl'

model = tf.keras.models.load_model('cnn_model.h5')
scaler_X = joblib.load('scaler_X.pkl')
scaler_y = joblib.load('scaler_y.pkl')
########################################
#  dataset de station info a preparer  #
########################################
FILE_PATH = 'merged_bike_44_weather_events.csv'
data = pd.read_csv(FILE_PATH)

# Preprocess dataset
data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
data['day_of_week'] = pd.to_datetime(data['timestamp']).dt.dayofweek
data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
data = data.set_index('timestamp')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.json
        hour = int(user_input.get('hour'))

        stations = data['number'].unique()
        features = []
        ######################
        ## context a fourni ##
        ######################:
        for station in stations:
            station_data = {
                'number': station,
                'status': 1, 
                'percentage_cloud_coverage': 0.5,  
                'visibility_distance': 10.0,       
                'percentage_humidity': 0.5,      
                'current_temperature': 15.0,     
                'feels_like_temperature': 14.0,   
                'is_rainy': 0,                   
                'hour': hour,
                'day_of_week': 0,                 
                'is_weekend': 0                   
            }
            features.append(list(station_data.values()))

        features_df = pd.DataFrame(features, columns=[
            'number', 'lat', 'lng', 'status', 'percentage_cloud_coverage',
            'visibility_distance', 'percentage_humidity', 'current_temperature',
            'feels_like_temperature', 'is_rainy', 'hour', 'day_of_week', 'is_weekend'
        ])

        X_scaled = scaler_X.transform(features_df)
        X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

        predictions = model.predict(X_scaled)
        y_pred = scaler_y.inverse_transform(predictions)

        response = []
        for station, bikes in zip(stations, y_pred.flatten()):
            response.append({
                'station': station,
                'available_bikes': round(bikes, 2)
            })

        return jsonify({'predictions': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
