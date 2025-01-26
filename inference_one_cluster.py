from flask import json
import pandas as pd
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import MeanAbsoluteError, MeanSquaredError

# obtenir le list 
clustered_stations_data = pd.read_csv('data/clustered_stations.csv')
clustered_stations = clustered_stations_data.groupby('cluster')['station'].apply(list).to_dict()


# Charger le scaler et le modèle
def load_all_model_scaler() :
    scalers_x = {0:load("scalers/scaler_X_cluster0.pkl"),
                 1:load("scalers/scaler_X_cluster1.pkl"),
                 2:load("scalers/scaler_X_cluster2.pkl"),
                 3:load("scalers/scaler_X_cluster3.pkl"),}
    models = {
        0: load_model("models_for_cluster/cnn_model_for_cluster0.h5", custom_objects={"mse": "mean_squared_error", "mae": "mean_absolute_error"}),
        1: load_model("models_for_cluster/cnn_model_for_cluster1.h5", custom_objects={"mse": "mean_squared_error", "mae": "mean_absolute_error"}),
        2: load_model("models_for_cluster/cnn_model_for_cluster2.h5", custom_objects={"mse": "mean_squared_error", "mae": "mean_absolute_error"}),
        3: load_model("models_for_cluster/cnn_model_for_cluster3.h5", custom_objects={"mse": "mean_squared_error", "mae": "mean_absolute_error"}),
    }
    return scalers_x,models

def get_cluster(number):
    for cluster, stations in clustered_stations.items():
        if number in stations:
            return cluster
    raise ValueError(f"Station number {number} does not belong to any cluster.")

def predict():
    scalers_x,models=load_all_model_scaler()
    data=load_data()
    # traiter les donnes commes dans le l'entrainement de model  
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['timestamp_numeric'] = data['timestamp'].astype('int64') // 10**9
    data['day_of_week'] = data['timestamp'].dt.dayofweek
    data['cluster'] = data['number'].apply(get_cluster)

    data = data.drop(columns=['timestamp', 'is_rainy'])  
    # Appliquer la standardisation sur 8 colones
    standardScale_feature = [
        'status', 'visibility_distance', 'current_temperature',
        'feels_like_temperature', 'wind_speed', 'counter_events',
        'timestamp_numeric', 'day_of_week'
    ]
    predictions = []
    grouped = data.groupby('cluster')
    for cluster, group in grouped:
        group=group.drop(columns='cluster')

        scaler_x = scalers_x[cluster]
        model = models[cluster]
        group[standardScale_feature] = scaler_x.transform(group[standardScale_feature])
        group_reshaped=group.to_numpy().reshape((group.shape[0], 1,  group.shape[1]))
        print(group_reshaped.shape)

        cluster_predictions = np.round(model.predict(group_reshaped)).astype(int)
        for number,prediction in zip(group['number'], cluster_predictions):
            print(f"cluster: {cluster},number: {number}, available_bikes: {int(prediction[0])}")

    
    return predictions
'''
def list_to_dataframe(data_list):
    columns = [
        'timestamp', 'number', 'status', 'bike_stands',
        'visibility_distance', 'current_temperature',
        'feels_like_temperature', 'is_rainy', 'wind_speed', 'counter_events'
    ]

    if len(data_list) != len(columns):
        raise ValueError(f"La liste doit contenir {len(columns)} éléments, mais {len(data_list)} ont été fournis.")
    df = pd.DataFrame([data_list], columns=columns)
    #print(df)
    return df
'''


def load_data():
    with open('data.json', 'r') as file:
        json_data = json.load(file)
        return pd.DataFrame(json_data)


'''
 timestamp              number  status  bike_stands  visibility_distance  current_temperature  feels_like_temperature  is_rainy  wind_speed  counter_events
2024-12-11 18:00:00      44       1           20              10000.0                 3.99                   1.255       0.0      11.105               2
'''

predict()

