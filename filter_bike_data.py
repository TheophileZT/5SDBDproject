
from collections import defaultdict
import csv
from datetime import datetime
import os

from outis import arrondi_heure, arrondi_second


def filter_all_bike_data(collection):
    try:
        documents = collection.find({}, {"timestamp": 1, "stationInfo": 1})

        filtered_data = []

        for doc in documents:
            station_info = doc.get("stationInfo", {})

            for station_name, station_data in station_info.items():
                status_station = 1 if station_data.get("status") == "OPEN" else 0
                position = station_data.get("position", {})
                station_entry = {
                    "timestamp": arrondi_second(doc.get("timestamp")),
                    "number": station_data.get("number"),
                    "lat": position.get("lat"),
                    "lng":position.get("lng"),
                    "status": status_station,
                    "available_bike_stands": station_data.get("available_bike_stands"),
                    "available_bikes": station_data.get("available_bikes"),
                    
                }
                filtered_data.append(station_entry)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données de vélos : {e}")
        return []
    

def bike_position_data(collection):
    try:
        # Récupérer un seul document (le premier)
        document = collection.find_one({}, {"stationInfo": 1})
        if not document:
            print("Aucun document trouvé.")
            return []

        filtered_data = []

        # Extraire les informations des stations à partir de stationInfo
        station_info = document.get("stationInfo", {})
        for station_name, station_data in station_info.items():
            position = station_data.get("position", {})
            station_entry = {
                "number": station_data.get("number"),
                "station_name": station_name,
                "lat": position.get("lat"),
                "lng":position.get("lng"),
            }
            filtered_data.append(station_entry)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données de vélos : {e}")
        return []

## filtrer les infos d'un velo indiqué et regrouper les entrées par heure
def filter_one_bike_data(collection,station_number):
    try:
        start_date = datetime.fromisoformat("2024-12-11T18:00:25.783+00:00")

        documents = collection.find(
            {"timestamp": {"$gt": start_date}},  
            {"timestamp": 1, "stationInfo": 1}
        )
        hourly_data = defaultdict(list) 

        for doc in documents:
            station_info = doc.get("stationInfo", {})

            for station_name, station_data in station_info.items():
                if station_data.get("number") == station_number:
                    status_station = 1 if station_data.get("status") == "OPEN" else 0
                    rounded_hour = arrondi_heure(doc.get("timestamp")) 
                    station_entry = {
                        "timestamp": arrondi_second(doc.get("timestamp")),
                        "number": station_data.get("number"),
                        "status": status_station,
                        "available_bike_stands": station_data.get("available_bike_stands"),
                        "available_bikes": station_data.get("available_bikes"),
                    }
                    hourly_data[rounded_hour].append(station_entry)
                    break

        averaged_data = []
        for hour, entries in hourly_data.items():
            total_bike_stands = sum(e["available_bike_stands"] for e in entries if e["available_bike_stands"] is not None)
            total_bikes = sum(e["available_bikes"] for e in entries if e["available_bikes"] is not None)
            total_status = sum(e["status"] for e in entries)
            total_number = sum(e["number"] for e in entries)

            count = len(entries)
            averaged_entry = {
                "hour": hour,
                "average_status": total_status / count,
                "average_bike_stands": total_bike_stands / count,
                "average_bikes": total_bikes / count,
                "average_number": total_number / count,
            }
            averaged_data.append(averaged_entry)

        return averaged_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données de vélos : {e}")
        return []

def load_stations_positions_from_csv(file_name):
    stations = []
    file_path = os.path.join("filtered_data", file_name)
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stations.append({
                "number": int(row["number"]),
                "station_name": row["station_name"],
                "lat": float(row["lat"]),
                "lng": float(row["lng"]),
            })
    return stations
 
