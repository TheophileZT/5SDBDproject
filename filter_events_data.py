## TODO : faut aussi generer les timestamp pour evenement pour match avec bikes et meteo

def filter_event_data(collection, stations):
    try:
        documents = collection.find(
            {}, 
            {
                "_id": 1,
                "nom_de_la_manifestation": 1,
                "date_debut": 1,
                "date_fin": 1,
                "googlemap_latitude": 1,
                "googlemap_longitude": 1,
            }
        )
 
        filtered_data = []
        for doc in documents:
            event_lat = doc.get("googlemap_latitude")
            event_lng = doc.get("googlemap_longitude")
            closest_stations = get_closest_stations(event_lat, event_lng, stations)
            '''# les colonnes pour les stations proches
            station_columns = {f"station_{i+1}": closest_stations[i] if i < len(closest_stations) else None 
                               for i in range(len(closest_stations))}
            '''
             
            event_entry = {
                "id_event": str(doc.get("_id")),   
                "date_debut": doc.get("date_debut"),
                "date_fin": doc.get("date_fin"),
                "event_lat": doc.get("googlemap_latitude"),
                "evant_lng": doc.get("googlemap_longitude"),
                "closest_stations": closest_stations,
            }
            # Ajouter les colonnes des stations proches
            ## event_entry.update(station_columns)
            filtered_data.append(event_entry)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données des événements : {e}")
        return []
    
import math

def get_closest_stations(event_lat, event_lng, stations, max_distance=0.5):
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calcule la distance en kilomètres entre deux points GPS avec la formule de Haversine.
        """
        R = 6371  # Rayon moyen de la Terre en kilomètres
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    closest_stations = []

    for station in stations:
        station_lat = station["lat"]
        station_lng = station["lng"]
        distance = haversine(event_lat, event_lng, station_lat, station_lng)

        if distance <= max_distance:
            closest_stations.append(station.get("number"))

    return closest_stations

