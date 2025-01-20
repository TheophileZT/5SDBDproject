import os
import shutil
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, explode, count

def merge_bike_weather_events(csv_bike, csv_weather, csv_events):
    # Chemins des fichiers CSV
    bike_path = os.path.join("filtered_data", csv_bike)
    weather_path = os.path.join("filtered_data", csv_weather)
    events_path = os.path.join("filtered_data", csv_events)

    # Initialiser une session Spark
    spark = SparkSession.builder \
        .appName("MergeBikeWeatherEvents") \
        .getOrCreate()

    # Charger les fichiers CSV dans des DataFrames Spark
    df_bike = spark.read.csv(bike_path, header=True, inferSchema=True)
    df_weather = spark.read.csv(weather_path, header=True, inferSchema=True)
    df_events = spark.read.csv(events_path, header=True, inferSchema=True)

    # Conversion des colonnes 'timestamp', 'date_debut', et 'date_fin' en format timestamp
    df_bike = df_bike.withColumn("timestamp", col("timestamp").cast("timestamp"))
    df_weather = df_weather.withColumn("timestamp", col("timestamp").cast("timestamp"))
    df_events = df_events \
        .withColumn("date_debut", col("date_debut").cast("timestamp")) \
        .withColumn("date_fin", col("date_fin").cast("timestamp"))

    # Étendre la liste des stations dans 'closest_stations'
    df_events = df_events.withColumn(
        "closest_stations", explode(expr("split(closest_stations, ',')"))
    )
    df_events = df_events.withColumn("closest_stations", col("closest_stations").cast("int"))

    # Fusionner les données de vélos et météo sur 'timestamp'
    df_bike_weather = df_bike.join(df_weather, on="timestamp", how="inner")

    # Ajouter les événements en fonction des plages horaires et des stations
    merged_df = df_bike_weather.join(
        df_events,
        (df_bike_weather["timestamp"] >= df_events["date_debut"]) &
        (df_bike_weather["timestamp"] <= df_events["date_fin"]) &
        (df_bike_weather["number"] == df_events["closest_stations"]),
        how="left"
    )

    # Ajouter une colonne pour compter les événements correspondants
    merged_df = merged_df.groupBy(
        df_bike_weather.columns  # Garder toutes les colonnes de df_bike_weather
    ).agg(
        count("closest_stations").alias("counter_events")
    )

    # Exportation du résultat dans un fichier CSV final
    bike_base = os.path.splitext(csv_bike)[0]
    output_name = f"merged_{bike_base}_weather_events.csv"
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
    
    # Arrêter la session Spark
    spark.stop()

    
