from collections import defaultdict
from datetime import datetime

import pandas as pd
from outis import arrondi_heure
#Génère des données toutes les 15 minutes en interpolant linéairement les données horaires.
def filter_weather_data(collection): 

    try:
        start_date = datetime.fromisoformat("2024-12-11T18:00:00.000+00:00")

        # Inclure tous les champs nécessaires dans la requête MongoDB
        documents = collection.find(
            {"timestamp": {"$gt": start_date}}, 
            {
            "timestamp": 1,
            "visibility.distance": 1,
            "temperature.current": 1,
            "temperature.feels_like": 1,
            "description": 1,  
            "wind":1,
        })
        hourly_data = []

        for doc in documents:
            # Vérifier si la description contient "rain"
            is_rainy = 1 if "rain" in (doc.get("description", "").lower()) else 0
            snow=1 if "snow" in (doc.get("description", "").lower()) else 0
            rounded_hour = arrondi_heure(doc.get("timestamp")) 
            # Préparer les données filtrées
            filtered_doc = {
                "hour": rounded_hour,
                ##"percentage_cloud_coverage": doc.get("cloud_coverage", {}).get("percentage"),
                "visibility_distance": doc.get("visibility", {}).get("distance"),
                ##"percentage_humidity": doc.get("humidity", {}).get("value"),
                "current_temperature": doc.get("temperature", {}).get("current"),
                "feels_like_temperature": doc.get("temperature", {}).get("feels_like"),
                "is_rainy": is_rainy,
                "snow":snow,
                ##"description":doc.get("description"),
                "wind_speed":doc.get("wind", {}).get("speed"),
                ##"pressure":doc.get("pressure", {}).get("current"),
                ##"sunrise":doc.get("local_times", {}).get("sunrise"),
                ##"sunset":doc.get("local_times", {}).get("sunset"),
            }
            hourly_data.append(filtered_doc)
        
        quarter_hourly_data = generate_quarter_hourly_data(hourly_data)

        return quarter_hourly_data
    
    except Exception as e:
        print(f"Erreur lors du filtrage des données : {e}")
        return []

##Génère des données toutes les 15 minutes en interpolant linéairement les données horaires.
def generate_quarter_hourly_data(hourly_data):
     
    try:
        # Convertir les données horaires en DataFrame pour faciliter l'interpolation
        df = pd.DataFrame(hourly_data)
        
        # Convertir 'hour' en objet datetime
        df['hour'] = pd.to_datetime(df['hour'])
        df.set_index('hour', inplace=True)

        # Convertir 'sunrise' et 'sunset' en timestamps pour permettre l'interpolation
        if 'sunrise' in df.columns:
            df['sunrise'] = pd.to_datetime(df['sunrise'], errors='coerce').astype('int64') // 1_000_000_000
        if 'sunset' in df.columns:
            df['sunset'] = pd.to_datetime(df['sunset'], errors='coerce').astype('int64') // 1_000_000_000
        
        
        # Générer un nouvel index avec des pas de 15 minutes
        new_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='15min')
        
        # Réindexer le DataFrame et interpoler linéairement les valeurs manquantes
        df = df.reindex(new_index)
        df = df.interpolate(method='linear')

        # Reconvertir les champs 'sunrise' et 'sunset' en datetime après interpolation
        if 'sunrise' in df.columns:
            df['sunrise'] = pd.to_datetime(df['sunrise'], unit='s', errors='coerce')
        if 'sunset' in df.columns:
            df['sunset'] = pd.to_datetime(df['sunset'], unit='s', errors='coerce')
            
        # Convertir en liste de dictionnaires
        interpolated_data = df.reset_index().rename(columns={'index': 'timestamp'}).to_dict(orient='records')
        return interpolated_data

    except Exception as e:
        print(f"Erreur lors de la génération des données : {e}")
        return []