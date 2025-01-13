import requests
from dotenv import load_dotenv
import os

import re

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

def match_stations(text):
    """Extract all stations thanks to extrapolated pattern (found by naked eye)

        Returns:
            unique_stations (list): A list of all found stations
        
        EXAMPLES :

        -> **Arrêts non desservis**

            - Le Lac Reynerie

        -> **Arrêts non desservis**

            Direction Basso Cambo :

            - Le Lac Reynerie

        -> **Arrêts non desservis** :

            - Compans-Caffarelli

        -> **Stations non desservies :**
                    
            Direction Palais de Justice  :

            - Déodat de Séverac
        
        -> **Arrêt non desservi**

            Direction Ramonville :

            - Parc du Canal
        
        -> Arrêt non desservi : La Lie - Lignes 103 et 107 du 06/12 au 18/12

    """
    # Regex pattern to extract station blocks
    # Very complicated
    pattern = r"(?i)(?:arrêts?|stations?)\s+non\s+desservie?s?(?:\*{2})?(?:\s*[:\-])?(?:\*{2})?\s*(?:(?:Direction\s+[^\n:]*:)?\s*(?:-\s*([^:]+)(?=\n)|([^\n-]+)(?:\s+-)?)+)"

    matches = re.findall(pattern, text)

    # Process each match to extract individual stations
    stations = []
    for match in matches:
        # Split station blocks into individual names
        for group in match:
            if group:
                # Split by newline to isolate station names
                stations.extend([station.strip() for station in group.split('\n') if station.strip()])

    # Remove station with numbers (regex pattern flaw) remove the extra dash in certain stations
    processed_stations = []
    for station in stations:
        # Numbers
        if re.search(r"[\d\"()]", station):
            continue
        # Dash
        if station.startswith('-'):
            station = station.split('-', 1)[-1].strip()
        processed_stations.append(station)

    unique_stations = sorted(set(processed_stations))

    return unique_stations

def disrupted_station_coordinates(message) :  
    """
    Fetches the coordinates of the disrupted station(s) from disruption message.
    
    Args:
        message (str): Message containing info about the disruption
        
    Returns:
        (x,y) (tuple): A tuple of x y coordinates of the station(s)

    """
    # Error handling mechanism
    if message == None:
        return None
   
    # Extract stations in message through regex
    stations = match_stations(message)
    coordinates = []

    ###################################### EXTRACTING COORDINATES ###########################################################
    for station in stations :
        base_url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/arrets-itineraire/records"

        # Fetch station info from API
        station_params = {
            "select": "geo_point_2d",
            "where": f"nom_arret = \"{station}\"",
        }
        station_response = requests.get(base_url, params=station_params)

        if station_response.status_code != 200:
            raise Exception(f"Failed to fetch disrupted stations for Toulouse: {station_response.status_code}")
        
        # Extract underlying station structure
        # TODO : make unique, cause duplicate for both ways
        station_coordinates = station_response.json().get("results", [])

        if station_coordinates : 
            lon = station_coordinates[0].get('geo_point_2d').get('lon')
            lat = station_coordinates[0].get('geo_point_2d').get('lat')
            coordinates.append((lat, lon))

            print(f"{station} : lat = {lat}, lon = {lon} ")

    return coordinates

my_message = """
# Ligne 19 : après 22h, demandez à descendre au plus près de chez vous !

**A compter du lundi 25 novembre 2024**, dans le cadre de la lutte contre le harcèlement sexiste et les violences sexuelles, Tisséo étend son service de " **_descente à la demande_**" à toutes les lignes soirée (hors Navette Aéroport).

Ainsi, la ligne **19** intègre ce dispositif qui vous permet, à partir de **22h00**, de demander à descendre entre 2 arrêts, au plus près de chez vous.

Retrouvez [**ICI**](https://www.tisseo.fr/info-tisseo/descente_a_la_demande_en_soiree) comment utiliser ce service ainsi que les autres lignes du dispositif.

# Arrêt non desservi : Lanusse - lignes 19 et 36

En raison de travaux, avenue Bourgès Maunoury à Toulouse, **d** **u mercredi 13 novembre** **au vendredi 13 décembre 2024,** l'arrêt " **Lanusse**" des lignes **19** et **36** en direction de **Borderouge** est non desservi.

Vous pouvez vous reporter à l'arrêt **"Montloup**".

Pour préparer votre déplacement et trouver la solution la plus adaptée, pensez au [calculateur d’itinéraire](https://plan-interactif.tisseo.fr/route-calculation).

# ⚠️ L19 : modification d'itinéraire au 16 septembre 2024

En raison des travaux d'aménagement pour la future **[ligne L12](https://www.tisseo.fr/se-deplacer/travaux-toulouse)**, chemin du Château de l'Hers à Toulouse, **du lundi 16 septembre au dimanche 22 décembre 2024 inclus** l'itinéraire de la ligne 19 est modifié.

Le terminus Place de l'Indépendance est reporté à [l'arrêt " **Coquille**"](https://plan-interactif.tisseo.fr/around?from=stop_area:SA_234&back=board), à 100 mètres de l'arrêt "Coquille" des lignes 23 / 37 / 51 situé avenue Jacques Chirac.

**Arrêt déplacé** :

- L'arrêt "Navarre" est reporté à l'arrêt "Navarre" de la ligne 51 situé avenue Jean Chaubet.

 **Arrêts non desservis** :

- Château de l'Hers (se reporter à l'arrêt "Navarre" situé avenue Jean Chaubet)
- Fontanelles
- Carcassonne
- Rougenet
- Illiade
- Ivoire
- Place de l'Indépendance

 Vos solutions de déplacement depuis l'avenue du Castres (à 10 minutes de marche maximum)

- ligne L1 : permet une correspondance avec la ligne B du métro à Jean Jaurès ou François Verdier
- ligne 37 : permet une correspondance avec la ligne A du métro à Jolimont et avec le nouveau terminus "Coquille" de la ligne 19.

Un plan et une nouvelle fiche horaire sont disponibles en pièce jointe de cette info.

Pour préparer votre déplacement et trouver la solution la plus adaptée, pensez au [calculateur d’itinéraires](https://plan-interactif.tisseo.fr/route-calculation) et à la rubrique [prochains passages](https://www.tisseo.fr/prochains-passages).
"""

disrupted_station_coordinates(my_message)

