from datetime import datetime

def arrondi_timestamp(timestamp):
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
