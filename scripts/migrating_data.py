""" 
    This script has been created a posteriori
    It has been used for data migration purposes

    The script is to be run locally. Make sure you update Data information with appropriate values

    # Main Functions :
    
    - connect_to_db(connection_string, db_name)

    ## Migration
        Data has been migrated from a collection to another mid work 

        - migrate_data(source_db, target_db)
            Migration logic
        - migration()
            Performs the migration

"""

from datetime import datetime
from dotenv import load_dotenv
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

from station_coordinates import disrupted_station_coordinates

def connect_to_db(connection_string, db_name):
    """
    Establishes a connection to the MongoDB database.
    Retuns db
    """
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        return db
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def migrate_data(source_db, target_db):
    """
    Migrates all data from the source database to the target database.

    Args:
        source_db (Database): The source MongoDB database.
        target_db (Database): The target MongoDB database.
    """
    try:
        collection_name = "Disruptions"
        print(f"Migrating collection: {collection_name}")
        source_collection = source_db[collection_name]
        target_collection = target_db[collection_name]

        # Fetch all documents from the source collection
        documents = list(source_collection.find())
        if documents:
            # Insert documents into the target collection
            target_collection.insert_many(documents)
            print(f"Migrated {len(documents)} documents from {collection_name}.")
        else:
            print(f"No documents found in {collection_name}, skipping.")
    except Exception as e:
        print(f"Error during migration: {e}")

def migration():
    """compare
    Main function to execute the migration.
    """
    # Connection strings
    source_connection_string = 'REPLACE WITH APPROPRIATE VALUE'
    target_connection_string = 'REPLACE WITH APPROPRIATE VALUE'

    # Database names
    source_db_name = 'REPLACE WITH APPROPRIATE VALUE'
    target_db_name = 'REPLACE WITH APPROPRIATE VALUE'

    # Connect to source and target databases
    source_db = connect_to_db(source_connection_string, source_db_name)
    target_db = connect_to_db(target_connection_string, target_db_name)

    if source_db != None and target_db != None:
        migrate_data(source_db, target_db)
        print("Migration completed successfully.")
    else:
        print("Failed to connect to one or both databases.")

if __name__ == "__main__":
    migration()
