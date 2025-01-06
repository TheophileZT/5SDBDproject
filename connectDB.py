import csv
import os
from pymongo import MongoClient
from config import (
    MONGO_URI_Theo,
    MONGO_DATABASE,
    MONGO_COLLECTION_Current_Weather,
    MONGO_COLLECTION_Bikes,
    MONGO_COLLECTION_Events
)
##from filter_bike_data import filter_all_bike_data,bike_position_data,filter_one_bike_data, load_stations_positions_from_csv

from filter_bike_data import bike_position_data, filter_all_bike_data, filter_one_bike_data, load_stations_positions_from_csv
from filter_events_data import filter_event_data, get_closest_stations
from filter_weather_data import filter_weather_data


def connect_to_mongodb(collection_name): 
    try:
        client = MongoClient(MONGO_URI_Theo)
        db = client[MONGO_DATABASE]
        collection = db[collection_name]
        print(f"Connexion réussie à la collection : {collection_name}")
        return collection
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB ou d'accès aux données : {e}")
        return None


def export_filtered_data(filtered_data, output_csv_name): 
    try:
        if not filtered_data:
            print("Aucune donnée à exporter.")
            return

        output_csv_path = os.path.join("filtered_data", output_csv_name)
        fieldnames = filtered_data[0].keys()

        with open(output_csv_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_data)

        print(f"Export {output_csv_path} avec succès.")
        print("---------------------------------------------")
    except Exception as e:
        print(f"Erreur lors de l'export des données : {e}")



def main():
    
    ## MONGO_COLLECTION_Current_Weather
    collectionWeather = connect_to_mongodb(MONGO_COLLECTION_Current_Weather)
    if collectionWeather is not None:
        filtered_data = filter_weather_data(collectionWeather)
        export_filtered_data(filtered_data, "weather_data_filtered.csv")
   
   
    ## MONGO_COLLECTION_Bikes
    collectionBikes = connect_to_mongodb(MONGO_COLLECTION_Bikes)
    if collectionBikes is not None:
        ## all bikes
        export_filtered_data(filter_all_bike_data(collectionBikes), "bikes_filtered.csv")
        
        ## Bikes_position ,et qui n'a pas besoin de mise a jour frequentiellement
        ##export_filtered_data(bike_position_data(collectionBikes), "bikes_position.csv")
        
        ## infos for one bike
        station_number=55
        file_name = f"bike_{station_number}.csv"
        export_filtered_data(filter_one_bike_data(collectionBikes,station_number),file_name)
   

   
    ## MONGO_COLLECTION_Events
    stations_positions = load_stations_positions_from_csv("bikes_position.csv")
    collectionEvents = connect_to_mongodb(MONGO_COLLECTION_Events)
    if collectionEvents is not None:
        filtered_data = filter_event_data(collectionEvents,stations_positions)
        export_filtered_data(filtered_data, "events_filtered.csv")
 
    

if __name__ == "__main__":
    main()
