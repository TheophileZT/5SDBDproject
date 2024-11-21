import requests
import csv
import sys
import os
import json

CSV_FILE = "evenements_culturels.csv"
CONFIG_FILE = 'config.json'

def usage(script_name, message):
    """
    Affiche le message d'erreur, rappelle l'usage possible du script et stoppe le script.
    """
    print(
        f"Erreur: {message}\n"
        "\n"
        f"Usage: {script_name} <ville>\n"
        "\n"
        " <ville> : Nom de la ville pour laquelle récupérer les événements.\n"
        " <date> : Date des evenements à récupérer (format AAAA-MM-JJ).\n"
        "\n"
        "Le nom de la ville doit correspondre à une ville configurée dans le fichier 'config.json'.\n",
        file=sys.stderr
    )
    sys.exit(1)

def read_arguments():
    """
    Vérifie la présence des arguments attendus
    et retourne leur valeur.
    Stoppe le script en cas d'erreur.
    """
    if len(sys.argv) != 3:
        usage(sys.argv[0], "Nombre d'arguments incorrect")
    city_name = sys.argv[1]
    date = sys.argv[2]
    return city_name, date


def load_config():
    """
    Charge le fichier de configuration JSON.
    """
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def get_city_config(city_name):
    """
    Retourne la configuration pour une ville donnée.
    """
    config = load_config()
    for city in config['villes']:
        if city['nom'].lower() == city_name.lower():
            return city
    print(f"Erreur : Ville '{city_name}' non trouvée dans la configuration.")
    return None

def fetch_events_from_api(api_url, limit):
    """
    Récupère les événements depuis l'API.
    """
    response = requests.get(f"{api_url}?order_by: date_debut&limit={limit}")
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return []  

# Lecture des événements depuis le fichier CSV
def read_events_from_csv():
    """
    Lit les événements existants depuis le fichier CSV.
    """
    events = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Utilise l'id_evenement_api comme clé
                events[row['id_evenement_api']] = row
    return events

def write_events_to_csv(events):
    """
    Écrit les événements dans le fichier CSV.
    """
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'id_evenement_api', 'ville_id', 'nom', 'description', 
            'date_debut', 'date_fin', 'latitude', 'longitude', 'adresse'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in events.values():
            writer.writerow(event)


def update_events(city_name):
    """
    Met à jour les événements pour une ville donnée en utilisant les données de l'API.
    """

    city_config = get_city_config(city_name)

    api_url = city_config['api_url']
    ville_id = city_config['ville_id']
    config = load_config()
    limit = config.get('limit', 100) # Récupère la limit (100 par défault)
    
    existing_events = read_events_from_csv()
    new_events = fetch_events_from_api(api_url, limit)

    for event in new_events:

        id_evenement_api = event.get('identifiant')
        nom = event.get('nom_de_la_manifestation')

        # Extraire les champs nécessaires
        event_data = {
            'id_evenement_api': id_evenement_api,
            'ville_id': ville_id,
            'nom': nom,
            'description': event.get('descriptif_court', '')[:255],
            'date_debut': event.get('date_debut', ''),
            'date_fin': event.get('date_fin', ''),
            'latitude': event.get('googlemap_latitude', ''),
            'longitude': event.get('googlemap_longitude', ''),
            'adresse': event.get('lieu_adresse_2', 'Adresse inconnue')
        }

        if id_evenement_api in existing_events:
            # Comparer les champs pour voir s'il y a eu des modifications
            if existing_events[id_evenement_api] != event_data:
                print(f"Mise à jour de l'événement : {nom}")
                existing_events[id_evenement_api] = event_data
        else:
            print(f"Ajout d'un nouvel événement : {nom}")
            existing_events[id_evenement_api] = event_data

    # Sauvegarder les événements mis à jour dans le CSV
    write_events_to_csv(existing_events)

if __name__ == "__main__":
    city_name = read_arguments()
    update_events(city_name)