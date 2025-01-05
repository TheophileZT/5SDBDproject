
def filter_bike_data(collection):
    try:
        documents = collection.find({}, {"timestamp": 1, "stationInfo": 1})

        filtered_data = []

        for doc in documents:
            timestamp = doc.get("timestamp")
            station_info = doc.get("stationInfo", {})

            

            for station_name, station_data in station_info.items():
                status_station = 1 if station_data.get("status") == "OPEN" else 0
                station_entry = {
                    "timestamp": timestamp,
                    "number": station_data.get("number"),
                    "station_name": station_name,
                    "position": station_data.get("position", {}),
                    "status": status_station,
                    "bike_stands": station_data.get("bike_stands"),
                    
                }
                filtered_data.append(station_entry)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données de vélos : {e}")
        return []
