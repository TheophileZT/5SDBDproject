import requests
import json
import pandas as pd
import argparse

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
            print(f"get {len(data)} station information succeed\n")
            return data
        else:
            print(f"error status: {response.status_code}\n")
            print(f"{response.text}")
            return None
    except Exception as e:
        print(f"error: {e}")
        return None



def save_to_csv_with_pandas(data, filename="stations_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="get bike station data for a specified city.")
    parser.add_argument("city", type=str, help="The name of the city (contract) to get data for.")
    args = parser.parse_args()
    contract = args.city
    print(f"get data for city: {contract}")
    station_data = fetch_station_data(contract)
    if station_data:
        save_to_csv_with_pandas(station_data, filename=f"{contract}_stations_data.csv")

if __name__ == "__main__":
    main()