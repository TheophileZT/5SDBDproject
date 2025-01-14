import ast
import os
import pandas as pd
import dask.dataframe as dd

 
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
    return output_name

 
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


def merger_bikesWeather_events(csv_bike_weather, csv_events_filtered):
    # Chemins des fichiers CSV
    bike_weather_path = os.path.join("filtered_data", csv_bike_weather)
    events_filtered_path = os.path.join("filtered_data", csv_events_filtered)

    # Lecture des fichiers CSV
    df_bikes_weather = dd.read_csv(bike_weather_path)
    df_events_filtered = dd.read_csv(events_filtered_path)

    # Conversion des colonnes 'timestamp', 'date_debut', et 'date_fin' en format datetime
    df_bikes_weather['timestamp'] = dd.to_datetime(df_bikes_weather['timestamp'])
    df_events_filtered['date_debut'] = dd.to_datetime(df_events_filtered['date_debut'])
    df_events_filtered['date_fin'] = dd.to_datetime(df_events_filtered['date_fin'])

    # Définition de la fonction pour compter les événements correspondants
    def count_matching_events(row, events_filtered):
        timestamp = row['timestamp']
        station_number = row['number']

        # Filtrer les événements actifs pour ce timestamp
        matching_events = events_filtered[
            (events_filtered['date_debut'] <= timestamp) &
            (events_filtered['date_fin'] >= timestamp)
        ]

        # Compter les événements dont la station est dans 'closest_stations'
        counter = 0
        for _, event in matching_events.iterrows():
            closest_stations = eval(event['closest_stations'])  # Convertir la chaîne en liste
            if station_number in closest_stations:
                counter += 1
        return counter

    # Application de la fonction avec map_partitions
    def apply_count_matching_events(partition):
        partition['counter_events'] = partition.apply(
            lambda row: count_matching_events(row, df_events_filtered.compute()),
            axis=1
        )
        return partition

    # Ajout de metadata pour que Dask puisse comprendre la structure des données
    meta = df_bikes_weather.head()
    meta['counter_events'] = 0  # Ajouter une colonne d'exemple pour le meta

    # Appliquer la fonction avec map_partitions et le meta défini
    df_bikes_weather = df_bikes_weather.map_partitions(apply_count_matching_events, meta=meta)

    # Exportation du résultat dans un nouveau fichier CSV
    bike_base = os.path.splitext(csv_bike_weather)[0]
    output_name = f"{bike_base}_events.csv"
    output_path = os.path.join("filtered_data", output_name)
    df_bikes_weather.compute().to_csv(output_path, index=False)
    print(f"Fichier fusionné exporté avec succès : {output_path}")