"""
This script fetches disrupted transport lines and their messages from an API, extracts relevant information including disruption periods, 
and stores the data in a MongoDB database. It also includes tools for visual inspection and debugging.
"""
import re
import dateparser.search
import requests
from datetime import datetime
import dateparser

import requests
import psycopg2
from datetime import datetime
import json

from dotenv import load_dotenv
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

from station_coordinates import adding_coordinates 

####################################### Configurations ####################################### 

load_dotenv()

# API configuration
API_CONFIG = {
    'Toulouse': { 
        'api_key': os.getenv("TISSEO_API_KEY"),
        'base_url': f'https://api.tisseo.fr/v2/',
    }
}

# Its Raphael's config that has DB Info
db_config_json= os.getenv("config_raph")

if not db_config_json:
    raise ValueError("db_config_json is required.")
try:
    DB_CONFIG = json.loads(db_config_json)
except json.JSONDecodeError as e:
    raise ValueError("Invalid JSON in for DB_CONFIG")

# Data structure
DATABASE_NAME =  DB_CONFIG["dbInfos"]["dbName"]
COLLECTION_NAME = "Disruptions"
client = None  # Declare client at the global level

# Define a list of cities
CITIES = ['Toulouse']
city_id = 0

# MongoDB connection
def connect_to_db():
    """
    Establishes a connection to the MongoDB database.
    Retuns db
    """
    connect_infos = {
        'connection_string': DB_CONFIG["dbInfos"]["uri"]
    }

    try:
        client = MongoClient(connect_infos['connection_string'])
        db = client[DATABASE_NAME]  # Database name
        return db
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None
    
####################################### Business Logic #######################################

# Function to save data to MongoDB
def save_to_db(db, collection_name, data):
    """
    Saves a list of records to a MongoDB collection.
    
    Args:
        db (Database): The database connection.
        collection_name (str): The name of the collection where data should be saved.
        data (list): A list of dictionaries containing the data
    """

    if db != None:
        collection = db[collection_name]
        try:
            for record in data:
                # Query to find an existing record with the same line_id
                existing_record = collection.find_one({'line_id': record['line_id']})
                
                if existing_record:
                    # Compare start_date and end_date
                    if (existing_record.get('start_date') == record['start_date'] or
                        existing_record.get('end_date') == record['end_date']):
                        # print(f"No changes for Line {record['line_id']}, skipping.")
                        continue  # Skip if both dates are the same

                    # Update the only end date if dates or other details changed
                    collection.update_one(
                        {'line_id': record['line_id']},
                        {'$set': {'end_date': record['end_date']}}
                    )
                    print(f"Updated Line {record['line_id']} with new dates.")
                else:
                    # Insert a new record if it doesn't exist
                    collection.insert_one(record)
                    print(f"Inserted new record for Line {record['line_id']}.")

        except Exception as e:
            print(f"Failed to save data to MongoDB: {e}")
    else:
        print("No database connection available.")


def close_connection():
    """Closes the MongoDB client connection."""
    if client:
        client.close()
        print("MongoDB connection closed.")

def fetch_disrupted_lines_and_messages(city):
    """
    Fetches disrupted transport lines and their corresponding messages for a given city.
    
    Args:
        city (str): The city for which to fetch disrupted lines.
        
    Returns:
        combined_info (list): A list of dictionaries containing line IDs, names, and messages.

    """

    # Fetch configuration for the city
    config = API_CONFIG.get(city)
    if not config:
        raise ValueError(f"No API configuration found for city: {city}")

    #######################################
    # Fetch disrupted lines
    lines_url = f"{config['base_url']}/lines.json"
    lines_params = {'displayOnlyDisrupted': '1', 'key': config['api_key']}
    lines_response = requests.get(lines_url, params=lines_params)

    if lines_response.status_code != 200:
        raise Exception(f"Failed to fetch disrupted lines for {city}: {lines_response.status_code}")
    # Extract underlying lines structure
    disrupted_lines = lines_response.json().get("lines", [])

    #######################################
    # Fetch messages
    messages_url = f"{config['base_url']}/messages.json"
    messages_params = {'key': config['api_key']}
    messages_response = requests.get(messages_url, params=messages_params)

    if messages_response.status_code != 200:
        raise Exception(f"Failed to fetch messages for {city}: {messages_response.status_code}")
    # Extract messages lines structure
    messages = messages_response.json().get("messages", [])
    
    
    #######################################
    # Create a dictionary mapping line_id to message content
    # Init
    message_dict = {}
    for message in messages:
        lines = message.get("lines", [])
        for line in lines:
            line_id = line.get("id")
            if line_id:  # Ensure there's an id present
                content =  message["message"]["content"]
                message_dict[line_id] = content

    # Combine disrupted lines with their corresponding messages
    combined_info = []
    for line in disrupted_lines["line"]:
        line_id = line["id"]
        message = message_dict.get(line_id)
        list_coordinates = adding_coordinates()

        combined_info.append({
            'id': line_id,
            'name': line['name'],
            'message': message,
            'gps_lat_lon': list_coordinates
        })


    return combined_info

def extract_dates_using_dateparser(text):
    """
    Extracts start and end dates from a natural language message.
    
    Args:
        text (str): The message text from which to extract dates.
        
    Returns:
        tuple: A tuple of start and end dates (datetime objects) or (None, None) if no valid dates are found.
    """
     
    # Dateparser detects dates in natural langage

    # Extract all dates using dateparser
    dates = dateparser.search.search_dates(text, languages=['fr'])

    # Filter out invalid or irrelevant dates using regex
    # For example, filter dates that are within a valid range or match a specific context (like "lundi")
    filtered_dates = []
    if dates:
        for _, date in dates:
            # Example: Filter out dates in the future that don't make sense in the context
            if date.tzinfo is not None:
                date = date.replace(tzinfo=None)
            if date and date.year <= 2025 and date.year>=2024:
                filtered_dates.append(date)

    # Sort the dates: earliest first for start date, latest for end date
    filtered_dates.sort()

    if len(filtered_dates) == 1:
            # If only one date is found, use today as the start date and the found date as the end date
             filtered_dates.append(datetime.today())

    # If multiple dates found, return the first and last
    if len(filtered_dates) >= 2:
        return filtered_dates[0], filtered_dates[-1]  # start_date end_date
    else:
        print("No valid dates found.")
        return None, None

def fetch_save_disruptions():

    db = connect_to_db()
    if db == None:
        print("Database connection failed. Exiting.")
        return
    
    # Fetch data
    lines_and_messages = fetch_disrupted_lines_and_messages("Toulouse")
    disruption_data = []

    print("\nProcessing disruption data:")
    for entry in lines_and_messages:
        line_id = entry['id']
        name = entry['name']
        message_text = entry['message']
        
        line_data = {
            'line_id': line_id,
            'line_name': name,
            'message': message_text,
            'start_date': None, # First initialized to None
            'end_date': None
        }

        if message_text:
            start, end = extract_dates_using_dateparser(message_text)
            if start and end:
                line_data['start_date'] = start.strftime('%Y-%m-%d')
                line_data['end_date'] = end.strftime('%Y-%m-%d')
            else:
                print(f"No valid dates found for Line {line_id}.")
        else:
            print(f"Line {line_id} has no associated message.")

        disruption_data.append(line_data)

    # Save data to MongoDB
    save_to_db(db, COLLECTION_NAME, disruption_data)
    close_connection()

def visual_test():
    """
    Debugging tool: Fetches and prints disrupted line data and associated messages for inspection.
    """

    # Fetch data
    lines_and_messages = fetch_disrupted_lines_and_messages("Toulouse")

    print("\nDisrupted lines and messages:")
    for element in lines_and_messages:
        print('##' * 100)
        print(f" - Line: {element['id']}")
        print(f" - Name: {element['name']}")
        print(f" - Message: {element['message']}\n\n")
        
    print("\nDisruption Messages and Periods:")
    for entry in lines_and_messages:
        line_id = entry['id']
        message_text = entry['message']

        if message_text:
            print(f"\nLine {line_id} - {entry['name']}")
            # Extract start and end dates from the message
            start, end = extract_dates_using_dateparser(message_text)
            
            if start and end:
                print(f"Start Date: {start.strftime('%Y-%m-%d')}")
                print(f"End Date: {end.strftime('%Y-%m-%d')}")
            else:
                print("No valid dates found.")
        else:
            print(f"\nLine {line_id} - {entry['name']}: No message available.")

if __name__ == "__main__":
    fetch_save_disruptions()
        
