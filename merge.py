import os

import pandas as pd

 
def merger_bikes_weather(csv1_name,csv2_name):
    
    csv1_path = os.path.join("filtered_data", csv1_name)
    csv2_path = os.path.join("filtered_data", csv2_name)
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Fusionner les deux DataFrames sur le champ 'timestamp'
    merged_df = pd.merge(df1, df2, on='timestamp', how='inner')  # 'inner' pour conserver uniquement les lignes correspondantes

    # Exporter le résultat dans un nouveau fichier CSV
    bike_base = os.path.splitext(csv1_name)[0]
    output_name = f"merged_{bike_base}_weather.csv"
    output_path = os.path.join("filtered_data", output_name)
    merged_df.to_csv(output_path, index=False)

    print(f"Fichier fusionné exporté avec succès : {output_path}")

 
def merger_bikes_weather_events(csv_bike, csv_weather, csv_events_filtered):
   
 # Chemins des fichiers CSV
    bike_path = os.path.join("filtered_data", csv_bike)
    weather_path = os.path.join("filtered_data", csv_weather)
    events_filtered_path = os.path.join("filtered_data", csv_events_filtered)

    # Lecture des fichiers CSV
    df_bikes = pd.read_csv(bike_path)
    df_weather = pd.read_csv(weather_path)
    df_events_filtered = pd.read_csv(events_filtered_path)

    # Conversion des colonnes 'timestamp', 'date_debut', et 'date_fin' en format datetime
    df_bikes['timestamp'] = pd.to_datetime(df_bikes['timestamp'])
    df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'])
    df_events_filtered['date_debut'] = pd.to_datetime(df_events_filtered['date_debut'])
    df_events_filtered['date_fin'] = pd.to_datetime(df_events_filtered['date_fin'])

    # Fusionner vélos et météo sur 'timestamp' 
    bikes_weather_df = pd.merge(df_bikes, df_weather, on='timestamp', how='inner')

    # Ajouter une colonne 'counter_events' pour compter les événements correspondants
    def count_matching_events(row):
        timestamp = row['timestamp']
        station_number = row['number']

        # Filtrer les événements qui sont actifs pour ce timestamp
        matching_events = df_events_filtered[
            (df_events_filtered['date_debut'] <= timestamp) & 
            (df_events_filtered['date_fin'] >= timestamp)
        ]

        # Compter les événements dont la station est dans 'closest_stations'
        counter = 0
        for _, event in matching_events.iterrows():
            closest_stations = eval(event['closest_stations'])  # Convertir la chaîne en liste
            if station_number in closest_stations:
                counter += 1
        return counter

    # ajouter une colonne 'counter_events'
    bikes_weather_df['counter_events'] = df_bikes.apply(count_matching_events, axis=1)

  

    # Exportation du résultat dans un nouveau fichier CSV
    bike_base = os.path.splitext(csv_bike)[0]
    output_name = f"merged_{bike_base}_weather_events.csv"
    output_path = os.path.join("filtered_data", output_name)
    bikes_weather_df.to_csv(output_path, index=False)
    print(f"Fichier fusionné exporté avec succès : {output_path}")