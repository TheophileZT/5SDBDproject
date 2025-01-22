import pandas as pd
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError, MeanSquaredError

# Charger le scaler et le modèle
def load_model_scaler() :
    scaler_x = load("scaler_X_one_station.pkl")
    model = load_model(
        "cnn_model_for_one_station.h5",
        custom_objects={
            "mse": MeanSquaredError(),
            "mae": MeanAbsoluteError()
        }
    )
    return scaler_x,model


def predict(data):
    scaler_x,model=load_model_scaler()
    data=list_to_dataframe(data)
    # traiter les donnes commes dans le l'entrainement de model  
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['timestamp_numeric'] = data['timestamp'].astype('int64') // 10**9
    data['day_of_week'] = data['timestamp'].dt.dayofweek
    data = data.drop(columns=['timestamp', 'is_rainy'])  

    # Appliquer la standardisation sur 8 colones
    standardScale_feature = [
        'status', 'visibility_distance', 'current_temperature',
        'feels_like_temperature', 'wind_speed', 'counter_events',
        'timestamp_numeric', 'day_of_week'
    ]
    data[standardScale_feature] = scaler_x.transform(data[standardScale_feature])
    data_reshaped = data.to_numpy().reshape((1, 1, data.shape[1]))

    # Effectuer la prédiction
    predictions = np.round(model.predict(data_reshaped)).astype(int)[0, 0]
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

