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

 
def merger_bikes_weather_events(csv_bike, csv_weather, csv_events_expanded):
   
    bike_path = os.path.join("filtered_data", csv_bike)
    weather_path = os.path.join("filtered_data", csv_weather)
    events_expanded_path = os.path.join("filtered_data", csv_events_expanded)

    # Lecture des fichiers CSV
    df_bikes = pd.read_csv(bike_path)
    df_weather = pd.read_csv(weather_path)
    df_events_expanded = pd.read_csv(events_expanded_path)

    # Conversion des colonnes 'timestamp' en format datetime
    df_bikes['timestamp'] = pd.to_datetime(df_bikes['timestamp'])
    df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'])
    df_events_expanded['timestamp'] = pd.to_datetime(df_events_expanded['timestamp'])

    # Grouper les événements par 'timestamp' pour obtenir nb_events et les stations associées
    grouped_events = (
        df_events_expanded.groupby('timestamp')
        .agg(
            nb_events=('id_event', 'count'),
            closest_stations=('closest_stations', lambda x: ', '.join(set(x)))
        )
        .reset_index()
    )

    # Fusion des données de vélos et de météo sur 'timestamp' avec une jointure interne
    bikes_weather_df = pd.merge(df_bikes, df_weather, on='timestamp', how='inner')

    # Ajouter les données des événements agrégés avec une jointure à gauche
    merged_df = pd.merge(bikes_weather_df, grouped_events, on='timestamp', how='left')

    # Remplir les valeurs NaN pour les colonnes ajoutées
    merged_df['nb_events'] = merged_df['nb_events'].fillna(0).astype(int)
    merged_df['closest_stations'] = merged_df['closest_stations'].fillna('null')

    # Exportation du résultat dans un nouveau fichier CSV
    bike_base = os.path.splitext(csv_bike)[0]
    output_name = f"merged_{bike_base}_weather_events.csv"
    output_path = os.path.join("filtered_data", output_name)
    merged_df.to_csv(output_path, index=False)
    print(f"Fichier fusionné et résumé exporté avec succès : {output_path}")
