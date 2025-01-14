
import os
import shutil
import pandas as pd
import dask.dataframe as dd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, count, expr

import os

 
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



def merger_bikes_weather_spark(csv1_name, csv2_name):
    # Chemins des fichiers CSV
    csv1_path = os.path.join("filtered_data", csv1_name)
    csv2_path = os.path.join("filtered_data", csv2_name)

    # Initialiser une session Spark
    spark = SparkSession.builder \
        .appName("MergerBikesWeather") \
        .getOrCreate()

    # Charger les fichiers CSV dans des DataFrames Spark
    df1 = spark.read.csv(csv1_path, header=True, inferSchema=True)
    df2 = spark.read.csv(csv2_path, header=True, inferSchema=True)

    # Conversion des colonnes 'timestamp' en format datetime
    df1 = df1.withColumn("timestamp", col("timestamp").cast("timestamp"))
    df2 = df2.withColumn("timestamp", col("timestamp").cast("timestamp"))

    # Fusionner les deux DataFrames sur le champ 'timestamp'
    merged_df = df1.join(df2, on="timestamp", how="inner")

    
    # Exporter le résultat dans un fichier CSV unique
    bike_base = os.path.splitext(csv1_name)[0]
    output_name = f"merged_{bike_base}_weather.csv"
    temp_output_path = os.path.join("filtered_data", "temp_output")
    final_output_path = os.path.join("filtered_data", output_name)

    # Utiliser .coalesce(1) pour rassembler toutes les partitions dans un seul fichier
    merged_df.coalesce(1).write.csv(temp_output_path, header=True, mode="overwrite")

    # Trouver le fichier exporté et le renommer en fichier final
    for filename in os.listdir(temp_output_path):
        if filename.startswith("part-") and filename.endswith(".csv"):
            shutil.move(os.path.join(temp_output_path, filename), final_output_path)

    # Supprimer le dossier temporaire
    shutil.rmtree(temp_output_path)
    print(f"Fichier fusionné exporté avec succès : {final_output_path}")
    return output_name


## merge evenement avec le fichier csv_bike_weather qui est deja mergé
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

 

def merger_bikesweather_events_spark(csv_bike_weather, csv_events_filtered):
    # Chemins des fichiers CSV
    bike_weather_path = os.path.join("filtered_data", csv_bike_weather)
    events_filtered_path = os.path.join("filtered_data", csv_events_filtered)

    # Initialiser une session Spark
    spark = SparkSession.builder \
        .appName("MergerBikesWeatherEvents") \
        .getOrCreate()

    # Charger les fichiers CSV dans des DataFrames Spark
    df_bikes_weather = spark.read.csv(bike_weather_path, header=True, inferSchema=True)
    df_events_filtered = spark.read.csv(events_filtered_path, header=True, inferSchema=True)

    # Conversion des colonnes 'timestamp', 'date_debut', et 'date_fin' en format timestamp
    df_bikes_weather = df_bikes_weather.withColumn("timestamp", col("timestamp").cast("timestamp"))
    df_events_filtered = df_events_filtered \
        .withColumn("date_debut", col("date_debut").cast("timestamp")) \
        .withColumn("date_fin", col("date_fin").cast("timestamp"))

    # Étendre la liste des stations dans 'closest_stations'
    df_events_filtered = df_events_filtered.withColumn(
        "closest_stations", explode(expr("split(closest_stations, ',')"))
    )
    df_events_filtered = df_events_filtered.withColumn("closest_stations", col("closest_stations").cast("int"))

    # Filtrer les événements pertinents pour chaque timestamp
    merged_df = df_bikes_weather.join(
        df_events_filtered,
        (df_bikes_weather["timestamp"] >= df_events_filtered["date_debut"]) &
        (df_bikes_weather["timestamp"] <= df_events_filtered["date_fin"]) &
        (df_bikes_weather["number"] == df_events_filtered["closest_stations"]),
        how="left"
    )

    # Ajouter une colonne pour compter les événements correspondants
    merged_df = merged_df.groupBy(
        df_bikes_weather.columns  # Garder toutes les colonnes de df_bikes_weather
    ).agg(
        count("closest_stations").alias("counter_events")
    )

    # Exportation du résultat dans un nouveau fichier CSV
    bike_base = os.path.splitext(csv_bike_weather)[0]
    output_name = f"{bike_base}_events.csv"
    temp_output_path = os.path.join("filtered_data", "temp_output")
    final_output_path = os.path.join("filtered_data", output_name)

    # Utiliser .coalesce(1) pour rassembler toutes les partitions dans un seul fichier
    merged_df.coalesce(1).write.csv(temp_output_path, header=True, mode="overwrite")

    # Trouver le fichier exporté et le renommer en fichier final
    for filename in os.listdir(temp_output_path):
        if filename.startswith("part-") and filename.endswith(".csv"):
            shutil.move(os.path.join(temp_output_path, filename), final_output_path)

    # Supprimer le dossier temporaire
    shutil.rmtree(temp_output_path)
    print(f"Fichier fusionné exporté avec succès : {final_output_path}")


 