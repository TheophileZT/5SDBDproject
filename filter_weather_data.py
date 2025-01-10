from collections import defaultdict
from outis import arrondi_heure

def filter_weather_data(collection): 
    try:
        # Inclure tous les champs nécessaires dans la requête MongoDB
        documents = collection.find({}, {
            "timestamp": 1,
            "cloud_coverage.percentage": 1,
            "visibility.distance": 1,
            "humidity.value": 1,
            "temperature.current": 1,
            "temperature.feels_like": 1,
            "description": 1,  # S'assurer que le champ description est inclus
        })
        hourly_data = defaultdict(list) 

        for doc in documents:
            # Vérifier si la description contient "rain"
            is_rainy = 1 if "rain" in (doc.get("description", "").lower()) else 0
            rounded_hour = arrondi_heure(doc.get("timestamp")) 
            # Préparer les données filtrées
            filtered_doc = {
                "percentage_cloud_coverage": doc.get("cloud_coverage", {}).get("percentage"),
                "visibility_distance": doc.get("visibility", {}).get("distance"),
                "percentage_humidity": doc.get("humidity", {}).get("value"),
                "current_temperature": doc.get("temperature", {}).get("current"),
                "feels_like_temperature": doc.get("temperature", {}).get("feels_like"),
                "is_rainy": is_rainy,
            }
            hourly_data[rounded_hour].append(filtered_doc)
            

        averaged_data = []
        for hour, entries in hourly_data.items():
            total_cloud_coverage = sum(e["percentage_cloud_coverage"] for e in entries if e["percentage_cloud_coverage"] is not None)
            total_visibility = sum(e["visibility_distance"] for e in entries if e["visibility_distance"] is not None)
            total_humidity = sum(e["percentage_humidity"] for e in entries if e["percentage_humidity"] is not None)
            total_current_temp = sum(e["current_temperature"] for e in entries if e["current_temperature"] is not None)
            total_feels_like_temp = sum(e["feels_like_temperature"] for e in entries if e["feels_like_temperature"] is not None)
            total_rainy = sum(e["is_rainy"] for e in entries)

            count = len(entries)
            averaged_entry = {
                "hour": hour,
                "average_cloud_coverage": total_cloud_coverage / count if count > 0 else None,
                "average_visibility_distance": total_visibility / count if count > 0 else None,
                "average_humidity": total_humidity / count if count > 0 else None,
                "average_current_temperature": total_current_temp / count if count > 0 else None,
                "average_feels_like_temperature": total_feels_like_temp / count if count > 0 else None,
                "rainy_ratio": total_rainy / count if count > 0 else None,  # Proportion des entrées "rainy"
            }
            averaged_data.append(averaged_entry)
        return averaged_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données : {e}")
        return []
