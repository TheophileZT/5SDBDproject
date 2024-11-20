import requests
import psycopg2
from datetime import datetime
import json

# TODO : get the endpoint
FUNCTIONALITY = "networks"

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
        'base_url': f'https://api.tisseo.fr/v2/{FUNCTIONALITY}.json',
    }
}

# Define a list of cities
CITIES = ['Toulouse']
