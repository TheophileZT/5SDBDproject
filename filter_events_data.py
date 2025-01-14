
    
import csv
from datetime import datetime, timedelta
import math
import os

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



def check_events_size(collection):
    size_events_local=0
    size_events_bdd=0
    ## Comptage depuis le csv locale 
    file_path = os.path.join("filtered_data", "events_filtered.csv")
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            size_events_local = sum(1 for _ in reader) 
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return False

    ## Comptage depuis la base de données
    try:
     size_events_bdd = collection.count_documents({})  # Méthode plus directe pour compter les documents
    except Exception as e:
        print(f"Erreur lors du filtrage des données des événements : {e}")
        return False

    print(f"size_events_local={size_events_local},et size_events_bdd={size_events_bdd}")
    return size_events_local==size_events_bdd


##on utilise plus
def generate_quarter_hourly_data_for_events(collection, stations):
    events_data= []
    if not check_events_size:
        events_data=filter_event_data(collection, stations)
        export_filtered_data(filtered_data, "events_filtered.csv")
    else:
        file_path = os.path.join("filtered_data", "events_filtered.csv")
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                events_data.append(row)

    # Générer des données toutes les 15 minutes
    quarter_hourly_data_events = []

    for event in events_data:
        try:
            event_id = event["id_event"]
            closest_stations = event["closest_stations"]
            
            # Transformer date_debut et date_fin en objets datetime
            start_date = datetime.strptime(event["date_debut"], "%Y-%m-%d")
            end_date = datetime.strptime(event["date_fin"], "%Y-%m-%d") + timedelta(days=1)  # Inclure la fin de journée

            current_time = start_date
            while current_time < end_date:
                quarter_hourly_data_events.append({
                    "id_event": event_id,
                    "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "closest_stations": closest_stations
                })
                current_time += timedelta(minutes=15)

        except Exception as e:
            print(f"Erreur lors de la génération des données pour l'événement {event['id_event']} : {e}")
            continue

    return quarter_hourly_data_events