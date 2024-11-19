import requests
import csv
import os

# URL de l'API pour récupérer les événements culturels
API_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/agenda-des-manifestations-culturelles-so-toulouse/records?order_by: date_debut&limit=100"

# Nom du fichier CSV où les événements seront stockés
CSV_FILE = "evenements_culturels.csv"

# Récupération des données depuis l'API
def fetch_events():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("Erreur lors de la récupération des données depuis l'API.")
        return []

# Lecture des événements depuis le fichier CSV
def read_events_from_csv():
    events = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Utilise l'id_evenement_api comme clé
                events[row['id_evenement_api']] = row
    return events

# Écriture des événements dans le fichier CSV
def write_events_to_csv(events):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'id_evenement_api', 'ville_id', 'nom', 'description', 
            'date_debut', 'date_fin', 'latitude', 'longitude', 'adresse'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in events.values():
            writer.writerow(event)

# Mise à jour des événements en fonction des données API
def update_events():
    # Récupérer les données existantes depuis le CSV
    existing_events = read_events_from_csv()

    # Récupérer les nouveaux événements depuis l'API
    new_events = fetch_events()

    for event in new_events:
        # Extraire les champs nécessaires
        id_evenement_api = event.get('identifiant')
        nom = event.get('nom_de_la_manifestation')
        description = event.get('descriptif_court', '')[:1000]  # On limite la description à 1000 caractères si nécessaire
        date_debut = event.get('date_debut')
        date_fin = event.get('date_fin')
        latitude = event.get('googlemap_latitude')
        longitude = event.get('googlemap_longitude')
        adresse = event.get('lieu_adresse_2', '')  # Adresse récupérée de lieu_adresse_2
        ville_id = 1  # On utilise un ID fixe pour Toulouse, à changer pour d'autres villes

        # Créer une entrée pour l'événement
        event_data = {
            'id_evenement_api': id_evenement_api,
            'ville_id': ville_id,
            'nom': nom,
            'description': description,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'latitude': latitude,
            'longitude': longitude,
            'adresse': adresse
        }

        # Vérifier si l'événement existe déjà (basé sur l'id_evenement_api)
        if id_evenement_api in existing_events:
            # Comparer les champs pour voir s'il y a eu des modifications
            if existing_events[id_evenement_api] != event_data:
                print(f"Mise à jour de l'événement : {nom}")
                existing_events[id_evenement_api] = event_data
        else:
            # Ajouter un nouvel événement
            print(f"Ajout d'un nouvel événement : {nom}")
            existing_events[id_evenement_api] = event_data

    # Sauvegarder les événements mis à jour dans le CSV
    write_events_to_csv(existing_events)

# Lancer la mise à jour des événements
update_events()