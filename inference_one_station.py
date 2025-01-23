import pandas as pd
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError, MeanSquaredError
# obtenir le list 
file_path = 'clustered_stations.csv'
clustered_stations_data = pd.read_csv(file_path)


clustered_stations = clustered_stations_data.groupby('cluster')['station'].apply(list).to_dict()


# Charger le scaler et le modèle
def load_all_model_scaler() :
    scalers_x = {0:load("scaler_X_one_station.pkl"),
                 1:load("scaler_X_one_station.pkl"),
                 2:load("scaler_X_one_station.pkl"),
                 3:load("scaler_X_one_station.pkl"),}
    models = {0: load_model(
        "cnn_model_for_one_station.h5",
        custom_objects={
            "mse": MeanSquaredError(),
            "mae": MeanAbsoluteError()}),
            1: load_model(
        "cnn_model_for_one_station.h5",
        custom_objects={
            "mse": MeanSquaredError(),
            "mae": MeanAbsoluteError()}),
            2:load_model(
        "cnn_model_for_one_station.h5",
        custom_objects={
            "mse": MeanSquaredError(),
            "mae": MeanAbsoluteError()}),
            3:load_model(
        "cnn_model_for_one_station.h5",
        custom_objects={
            "mse": MeanSquaredError(),
            "mae": MeanAbsoluteError()})
    }
    return scalers_x,models

def get_cluster(number):
    for cluster, stations in clustered_stations.items():
        if number in stations:
            return cluster
    raise ValueError(f"Station number {number} does not belong to any cluster.")

def predict(data):
    scalers_x,models=load_all_model_scaler()
    data=list_to_dataframe(data)
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
        scaler_x = scalers_x[cluster]
        model = models[cluster]
        group[standardScale_feature] = scaler_x.transform(group[standardScale_feature])
        group_reshaped = group[standardScale_feature].to_numpy().reshape((group.shape[0], 1, len(standardScale_feature)))
        cluster_predictions = np.round(model.predict(group_reshaped)).astype(int).flatten()
        for number, prediction in zip(group['number'], cluster_predictions):
            predictions.append({'number': number, 'prediction': prediction})
    print("Prédictions :", predictions)
    return predictions

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
 timestamp              number  status  bike_stands  visibility_distance  current_temperature  feels_like_temperature  is_rainy  wind_speed  counter_events
2024-12-11 18:00:00      44       1           20              10000.0                 3.99                   1.255       0.0      11.105               2
'''
data=['2024-12-11 18:00:00',44,1,20,10000.0,3.99,1.255,0.0,11.105,2]
predict(data)

