import csv
from pymongo import MongoClient

# Connessione a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Antiriciclaggio']

# Lettura dei dati dal file CSV
transactions_data = []
with open('transactions.csv', 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        transactions_data.append({
            'id': row['id'],
            'Mittente': row['Mittente'],
            'Destinatario': row['Destinatario'],
            'Importo': int(row['Importo']),
            'Data': row['Data']
        })

# Inserimento dei dati in MongoDB
datasets = {
    'Db_25': transactions_data[:int(len(transactions_data) * 0.25)],
    'Db_50': transactions_data[:int(len(transactions_data) * 0.50)],
    'Db_75': transactions_data[:int(len(transactions_data) * 0.75)],
    'Db_100': transactions_data
}

# Inserimento dei dati nei diversi dataset
for collection_name, dataset in datasets.items():
    collection = mongo_db[collection_name]
    collection.insert_many(dataset)
print("Dataset caricati in MongoDb con successo")

