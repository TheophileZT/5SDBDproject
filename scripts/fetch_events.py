import requests
import sys
import json
from pymongo import MongoClient

CONFIG_FILE = 'config.json'

uri="mongodb+srv://theozt25:MGZ7Osyw7gMrGU4O@integratorproject.5ulkz.mongodb.net/"
dbName="DB"
collectionName="Events"
limit=100

def save_to_mongodb(data, mongo_uri, database_name, collection_name):
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        updated_count = 0
        inserted_count = 0

        for record in data:
            
            identifiant = record.get('identifiant')  
            if not identifiant:
                print("Record missing 'identifiant', skipping:", record)
                continue

            # Mise à jour ou insertion
            result = collection.update_one(
                {"identifiant": identifiant},  
                {"$set": record},       
                upsert=True             
            )

            # Comptabiliser les résultats
            if result.matched_count > 0:
                updated_count += 1
            elif result.upserted_id is not None:
                inserted_count += 1

        print(f"Data saved successfully to MongoDB in database '{database_name}', collection '{collection_name}'.")
        print(f"Documents updated: {updated_count}, Documents inserted: {inserted_count}")
   
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

def fetch_events_from_api(limit):
    """
    Récupère les événements depuis l'API.
    """
    response = requests.get(f"https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/agenda-des-manifestations-culturelles-so-toulouse/records?order_by: date_debut&limit={limit}")
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return []

def update_events(city_name):
    """
    Met à jour les événements pour une ville donnée en utilisant les données de l'API.
    """
    new_events = fetch_events_from_api(limit)

    # Sauvegarde les nouveaux événements dans la base de données
    save_to_mongodb(new_events, uri, dbName, collectionName)

if __name__ == "__main__":
    city_name = read_arguments()
    update_events(city_name)
