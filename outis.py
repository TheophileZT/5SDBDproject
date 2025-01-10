from datetime import datetime

def arrondi_second(timestamp):
    '''
      if isinstance(timestamp, str):
        # Convertir en objet datetime si le timestamp est une chaîne
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    '''
   
    if isinstance(timestamp, datetime):
        # Remettre les secondes et microsecondes à zéro
        rounded_timestamp = timestamp.replace(second=0, microsecond=0)
        return rounded_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return None 

def arrondi_heure(timestamp):
    """
    Fonction pour arrondir un timestamp à l'heure la plus proche.
    """
    if isinstance(timestamp, datetime):
        timestamp = int(timestamp.timestamp())  # Convertir datetime en timestamp Unix
    dt = datetime.fromtimestamp(timestamp)  # Assurez-vous que le timestamp est en secondes
    return dt.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")