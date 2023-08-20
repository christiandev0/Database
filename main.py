from pymongo import MongoClient


# Connessione a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Antiriciclaggio']  # Cambia il nome del database se necessario


# Chiudi la connessione
mongo_client.close()
