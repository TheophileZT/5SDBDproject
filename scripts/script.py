import requests
import psycopg2
from datetime import datetime
import json

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Database configuration TODO : Update
DB_CONFIG = {
    'dbname': 'metro_monitoring',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 0,
}

# API configuration
API_CONFIG = {
    'Toulouse': {
        'api_key': 'e9a7d698-8e62-4400-b0e3-8167d2971b57', # TODO : Setup as githubsecret
        'base_url': f'https://api.tisseo.fr/v2/',
    }
}

# Define a list of cities
CITIES = ['Toulouse']

# Database connection
def connect_to_db():

    connectInfos = {
        'connection_string': 'mongodb+srv://theozt25:MGZ7Osyw7gMrGU4O@project.5ulkz.mongodb.net/'
    }

    try:
        client = MongoClient(connectInfos['connection_string'])
        db = client.sample_mflix
        print(db)
        print("Connected to MongoDB")
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()

# Once you extract a disruptions
# Fetch the corresponding messages through name attribute
# Parse and save events into the database

# Fetch transport events from the API
def fetch_dirupted_lines(city):
    FUNCTIONALITY = "lines"
    config = API_CONFIG.get(city)
    if not config:
        raise ValueError(f"No API configuration found for city: {city}")
    
    url = f"{config['base_url']}/lines.json"
    params = {'displayOnlyDisrupted': '1', 'key': config['api_key']}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {city}: {response.status_code}")
    
    return response.json()

# Testing response
print(fetch_dirupted_lines("Toulouse"))

# Fetch messages TODO: Need to fetch message corresponding to disrupted lines
def fetch_messages(city):
    FUNCTIONALITY = "messages"

    config = API_CONFIG.get(city)

    if not config:
        raise ValueError(f"No API configuration found for city: {city}")
    
    url = f"{config['base_url']}/messages.json"
    params = {'key': config['api_key']}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch messages: {response.status_code}")
    return response.json()

# Save events to the database
def save_events(city_id, lines, messages):
    # TODO : Don't update already existing entries

    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert or update line disruptions
    for line in lines.get("lines", []):
        line_id = line["id"]
        disruption_messages = line.get("messages", [])
        for message in disruption_messages:
            message_id = message["id"]
            content = message.get("text", "")
            cursor.execute("""
                INSERT INTO probleme_transport (probleme_transport_id, ville_id, nom, description, date_debut, date_fin, zone_impactee)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (probleme_transport_id) DO UPDATE
                SET description = EXCLUDED.description
            """, (message_id, city_id, line["name"], content, datetime.now(), None, line_id))

    # Insert or update general messages
    for msg in messages.get("messages", []):
        message_id = msg["id"]
        content = msg.get("text", "")
        cursor.execute("""
            INSERT INTO probleme_transport (probleme_transport_id, ville_id, nom, description, date_debut, date_fin, zone_impactee)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (probleme_transport_id) DO UPDATE
            SET description = EXCLUDED.description
        """, (message_id, city_id, "General Message", content, datetime.now(), None, None))

    conn.commit()
    cursor.close()
    conn.close()

# Main process
def monitor_disruptions():
    city_id = 0  # Toulouse
    try:
        print("Fetching disrupted lines...")
        disrupted_lines = fetch_dirupted_lines(CITIES[city_id])
        print("Fetching messages...")
        messages = fetch_messages(CITIES[city_id])
        print("Saving events to the database...")
        #save_events(city_id, disrupted_lines, messages)
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_to_db()
    monitor_disruptions()
