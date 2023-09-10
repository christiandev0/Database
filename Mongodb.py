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
            'Data': row['Data'],
            'Metodo_di_pagamento': row['Metodo_di_pagamento'],
            'Valuta': row['Valuta'],
            'Paese_del_Cliente': row['Paese_del_Cliente'],
            'Paese_a_Rischio': row['Paese_a_Rischio'],
            'Mittente_sospetto': row['Mittente_sospetto'],
            'Destinatario_sospetto': row['Destinatario_sospetto']
        })

# Inserimento dei dati in MongoDB
datasets = {
    'Transazione_25': transactions_data[:int(len(transactions_data) * 0.25)],
    'Transazione_50': transactions_data[:int(len(transactions_data) * 0.50)],
    'Transazione_75': transactions_data[:int(len(transactions_data) * 0.75)],
    'Transazione_100': transactions_data
}
# Creazione e inserimento dei documenti per i nodi Mittente
for dataset_name, dataset in datasets.items():
    mittente_collection = mongo_db[f'Mittente_{dataset_name}']
    for transaction in dataset:
        mittente_collection.insert_one({
            'id': transaction['id'],
            'Nome': transaction['Mittente']
        })

# Creazione e inserimento dei documenti per i nodi Destinatario
for dataset_name, dataset in datasets.items():
    destinatario_collection = mongo_db[f'Destinatario_{dataset_name}']
    for transaction in dataset:
        destinatario_collection.insert_one({
            'id': transaction['id'],
            'Nome': transaction['Destinatario']
        })

# Inserimento dei dati nei diversi dataset
for collection_name, dataset in datasets.items():
    collection = mongo_db[collection_name]
    collection.insert_many(dataset)
print("Dataset caricati in MongoDb con successo")

