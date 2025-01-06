
def filter_weather_data(collection): 
    try:
        documents = collection.find({}, {
            "timestamp": 1,
            "cloud_coverage.percentage": 1,
            "visibility.distance": 1,
            "humidity.value": 1,
            "temperature.current": 1,
            "temperature.feels_like": 1,
        })
        filtered_data = []

        ## verifier si vraiment pleut dans l'inscription
        for doc in documents:
            # Extraire uniquement les champs nécessaires
            filtered_doc = {
                "timestamp": doc.get("timestamp"),
                "percentage_cloud_coverage": doc.get("cloud_coverage", {}).get("percentage"),
                "visibility_distance": doc.get("visibility", {}).get("distance"),
                "percentage_humidity": doc.get("humidity", {}).get("value"),
                "current_temperature": doc.get("temperature", {}).get("current"),
                "feels_like_temperature": doc.get("temperature", {}).get("feels_like"),
            }
            filtered_data.append(filtered_doc)

        return filtered_data

    except Exception as e:
        print(f"Erreur lors du filtrage des données : {e}")
        return []