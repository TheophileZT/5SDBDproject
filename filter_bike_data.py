
def filter_all_bike_data(collection):
    try:
        documents = collection.find({}, {"timestamp": 1, "stationInfo": 1})

        filtered_data = []

        for doc in documents:
            timestamp = doc.get("timestamp")
            station_info = doc.get("stationInfo", {})

            for station_name, station_data in station_info.items():
                status_station = 1 if station_data.get("status") == "OPEN" else 0
                position = station_data.get("position", {})
                station_entry = {
                    "timestamp": timestamp,
                    "number": station_data.get("number"),
                    "lat": position.get("lat"),
                    "lng":position.get("lng"),
                    "status": status_station,
                    "bike_stands": station_data.get("bike_stands"),
                    
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


def filter_one_bike_data(collection,station_number):
    try:
        documents = collection.find({}, {"timestamp": 1, "stationInfo": 1})

        filtered_data = []

        for doc in documents:
            timestamp = doc.get("timestamp")
            station_info = doc.get("stationInfo", {})

            for station_name, station_data in station_info.items():
                if station_data.get("number") == station_number:
                    status_station = 1 if station_data.get("status") == "OPEN" else 0
                    ##position = station_data.get("position", {})
                    station_entry = {
                        "timestamp": timestamp,
                        "number": station_data.get("number"),
                       ## "lat": position.get("lat"),
                       ## "lng": position.get("lng"),
                        "status": status_station,
                        "bike_stands": station_data.get("bike_stands"),
                    }
                    filtered_data.append(station_entry)
                    break


        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données de vélos : {e}")
        return []
    