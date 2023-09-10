import csv
from pymongo import MongoClient
import time
import statistics
import openpyxl
import scipy.stats

# Connessione a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Antiriciclaggio']

# Definizione delle collezioni
mongo_collection_25 = mongo_db['Transazioni_25']
mongo_collection_50 = mongo_db['Transazioni_50']
mongo_collection_75 = mongo_db['Transazioni_75']
mongo_collection_100 = mongo_db['Transazioni_100']

# Definizione dei dataset
collections = {
    '25%': mongo_collection_25,
    '50%': mongo_collection_50,
    '75%': mongo_collection_75,
    '100%': mongo_collection_100
}
# Query 1
query_1 = [
    {
        'Importo': {'$lt': 1000},
        'Paese_a_Rischio': 'Sì',
        'Metodo_di_pagamento': {'$ne': 'Carta di credito'}
    }
]

# Query 2
query_2 = [
    {
        '$or': [
            {'Importo': {'$gt': 2000}},
            {
                '$and': [
                    {'Paese_a_Rischio': 'Sì'},
                    {'Metodo_di_pagamento': 'Bonifico'},
                    {'Data': {'$lt': '2023-06-30T00:00:00Z'}}
                ]
            }
        ]
    }
]

# Query 3
query_3 = [
    {
        '$or': [
            {
                '$and': [
                    {'Paese_a_Rischio': 'Sì'},
                    {'Importo': {'$gt': 1500}}
                ]
            },
            {
                '$and': [
                    {'Paese_a_Rischio': 'No'},
                    {'Metodo_di_pagamento': {'$ne': 'PayPal'}}
                ]
            }
        ],
        'Data': {'$gte': '2023-01-01T00:00:00Z', '$lte': '2023-12-31T23:59:59Z'}
    }
]

# Query 4
query_4 = [
    {
        '$or': [
            {
                '$and': [
                    {'Paese_a_Rischio': 'Sì'},
                    {
                        '$or': [
                            {'Mittente_sospetto': 'Si'},
                            {'Destinatario_sospetto': 'Si'}
                        ]
                    }
                ]
            },
            {
                '$and': [
                    {'Importo': {'$gt': 1500}},
                    {'Metodo_di_pagamento': 'Assegno'},
                    {'Data': {'$gt': '2023-09-15T00:00:00Z'}}
                ]
            }
        ]
    },
    {
        '$unwind': '$Destinatario'
    },
    {
        '$lookup': {
            'from': 'Destinatario',
            'localField': 'Destinatario',
            'foreignField': 'Nome',
            'as': 'DestinatarioData'
        }
    },
    {
        '$group': {
            '_id': '$_id',
            'Transazione': {'$first': '$$ROOT'},
            'Destinatario': {'$first': {'$arrayElemAt': ['$DestinatarioData', 0]}}
        }
    }
]

# Lista delle query
queries = {
    'Query 1': query_1,
    'Query 2': query_2,
    'Query 3': query_3,
    'Query 4': query_4
}


# Funzione per eseguire la query
def execute_query(collection, query):
    def wrapper():
        result = list(collection.find(query))  # Converte il risultato in una lista
        print(result)
        return result  # Restituisce il risultato della query

    return wrapper


# Numero di esecuzioni per ogni query e dataset
num_executions = 31

# Apertura del file CSV per i risultati
with open('Risultati_esperimenti_MongoDB.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        ['Query', 'Database', 'First Execution Time (ms)', 'Average Execution Time (ms)', 'Confidence Interval (95%)'])
    # Esecuzione degli esperimenti e registrazione dei risultati nel file CSV
    for query_name, query_list in queries.items():
        for dataset_percentage, collection in collections.items():
            print(f"Query: {query_name}, Dataset: {dataset_percentage}")
            single_query_times = []
            for _ in range(num_executions):
                query_func = execute_query(collection, query_list[0])
                start_time = time.perf_counter()
                query_func()  # Esecuzione effettiva della query
                elapsed_time = (time.perf_counter() - start_time) * 1000  # Tempo in millisecondi
                single_query_times.append(elapsed_time)

            avg_time = statistics.mean(single_query_times)
            confidence_interval = scipy.stats.t.interval(0.95, len(single_query_times) - 1, loc=avg_time,
                                                         scale=scipy.stats.sem(single_query_times))
            # Scrittura dei risultati nel file CSV
            csvwriter.writerow([query_name, dataset_percentage, single_query_times[0], avg_time,
                                f'({confidence_interval[0]}, {confidence_interval[1]})'])

            print(f"  Tempo medio: {avg_time:.2f} ms")
            print(f"  Intervallo di confidenza: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")

# Chiusura del file CSV
csvfile.close()

# Chiusura della connessione
mongo_client.close()
