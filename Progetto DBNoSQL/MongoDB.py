
import pandas as pd
from pymongo import MongoClient

# Connessione al database MongoDb
client = MongoClient('mongodb://localhost:27017/')
db = client['Antiriciclaggio']

# Percentuali dei dataset rispetto al 100%
collections_percentages = [100, 75, 50, 25]

# Tipi di dati
collections = ['mittenti', 'destinatari', 'transazioni']

for data_type in collections:
    for percentage in collections_percentages:
        csv_filename = f'{data_type}_{percentage}%.csv'

        # Legge i dati dal file CSV utilizzando pandas
        data = pd.read_csv(csv_filename, encoding='ISO-8859-1')

        # Converte i dati in formato JSON
        data_json = data.to_dict(orient='records')

        # Inserisce i dati nella collezione del database
        collection_name = f'{data_type}{percentage}%'
        collection = db[collection_name]
        collection.insert_many(data_json)

        print(f"Dati del dataset {collection_name} inseriti in MongoDB con successo!.")

print("Inserimento completato per tutti i dataset.")
