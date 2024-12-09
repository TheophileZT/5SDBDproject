import requests
import sys
import json
from pymongo import MongoClient

CONFIG_FILE = 'config.json'

uri="mongodb+srv://theozt25:MGZ7Osyw7gMrGU4O@project.5ulkz.mongodb.net/"
dbName="myDatabase"
collectionName="Events"

def save_to_mongodb(data, mongo_uri, database_name, collection_name):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        collection.insert_many(data)

        print(f"Data saved successfully to MongoDB in database '{database_name}', collection '{collection_name}'.\n")
    except Exception as e:
        print(f"Error while saving to MongoDB: {e}")
    finally:
        client.close()

def usage(script_name, message):
    """
    Affiche le message d'erreur, rappelle l'usage possible du script et stoppe le script.
    """
    print(
        f"Erreur: {message}\n"
        "\n"
        f"Usage: {script_name} <ville>\n"
        "\n"
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
    if len(sys.argv) != 2:
        usage(sys.argv[0], "Nombre d'arguments incorrect")
    city_name = sys.argv[1]
    return city_name

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

def update_events(city_name):
    """
    Met à jour les événements pour une ville donnée en utilisant les données de l'API.
    """
    city_config = get_city_config(city_name)

    if not city_config:
        return

    api_url = city_config['api_url']
    config = load_config()
    limit = config.get('limit', 100)  # Récupère la limite (100 par défaut)

    new_events = fetch_events_from_api(api_url, limit)

    # Sauvegarde les nouveaux événements dans la base de données
    save_to_mongodb(new_events, uri, dbName, collectionName)

if __name__ == "__main__":
    city_name = read_arguments()
    update_events(city_name)
