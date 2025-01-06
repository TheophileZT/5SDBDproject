from outis import arrondi_timestamp

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
        filtered_data = []

        for doc in documents:
            # Vérifier si la description contient "rain"
            is_rainy = 1 if "rain" in (doc.get("description", "").lower()) else 0

            # Préparer les données filtrées
            filtered_doc = {
                "timestamp": arrondi_timestamp(doc.get("timestamp")),
                "percentage_cloud_coverage": doc.get("cloud_coverage", {}).get("percentage"),
                "visibility_distance": doc.get("visibility", {}).get("distance"),
                "percentage_humidity": doc.get("humidity", {}).get("value"),
                "current_temperature": doc.get("temperature", {}).get("current"),
                "feels_like_temperature": doc.get("temperature", {}).get("feels_like"),
                "is_rainy": is_rainy,
                ##"description": doc.get("description", ""),  
            }
            filtered_data.append(filtered_doc)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données : {e}")
        return []
