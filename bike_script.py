import requests
import argparse
from pymongo import MongoClient

API_URL = "https://api.jcdecaux.com/vls/v1/stations"
API_KEY = "747abc58543245b99b316a08dece9b29bd42662d"


def fetch_station_data(contract):
    try:
        params = {
            "contract": contract,
            "apiKey": API_KEY
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Get {len(data)} station information succeeded\n")
            return data
        else:
            print(f"Error status: {response.status_code}\n")
            print(f"{response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_mongodb(data, contract, mongo_uri, database_name, collection_name):
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


def main():
    parser = argparse.ArgumentParser(description="Get bike station data for a specified city and save to MongoDB.")
    parser.add_argument("city", type=str, help="The name of the city (contract) to get data for.")
    parser.add_argument("--mongo_uri", type=str, default="mongodb://localhost:27017", help="MongoDB connection URI.")
    parser.add_argument("--db", type=str, required=True, help="MongoDB database name.")
    parser.add_argument("--collection", type=str, required=True, help="MongoDB collection name.")
    args = parser.parse_args()

    contract = args.city
    mongo_uri = args.mongo_uri
    database_name = args.db
    collection_name = args.collection

    print(f"Fetching data for city: {contract}")
    station_data = fetch_station_data(contract)
    if station_data:
        save_to_mongodb(station_data, contract, mongo_uri, database_name, collection_name)

if __name__ == "__main__":
    main()
