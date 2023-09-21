import csv
import statistics
import time

import scipy
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Antiriciclaggio']

# Lista delle percentuali
percentages = ['100%', '75%', '50%', '25%']

# Definizione delle collezioni
collection_names = {
    '25%': {
        'transazioni': 'transazioni25%',
        'destinatari': 'destinatari25%',
        'mittenti': 'mittenti25%',
    },
    '50%': {
        'transazioni': 'transazioni50%',
        'destinatari': 'destinatari50%',
        'mittenti': 'mittenti50%',
    },
    '75%': {
        'transazioni': 'transazioni75%',
        'destinatari': 'destinatari75%',
        'mittenti': 'mittenti75%',
    },
    '100%': {
        'transazioni': 'transazioni100%',
        'destinatari': 'destinatari100%',
        'mittenti': 'mittenti100%',
    }
}

csv_filename = 'Risultati_esperimenti_MongoDB.csv'
num_executions = 31

# Apertura del file CSV per la scrittura
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Query', 'Dataset', 'Prima Esecuzione (ms)', 'Media Esecuzioni Successive (ms)', 'Confidence '
                                                                                                         'Interval ('
                                                                                                         '95%)'])

    # Esecuzione degli esperimenti e registrazione dei risultati nel file CSV
    for percentage in percentages:
        transazioni = f'transazioni{percentage}'
        print(transazioni)
        print(f"Analisi per la percentuale: {percentage}")
        # Verifica le collezioni nel database
        print(db.list_collection_names())
        # Query 1: Conteggio delle transazioni sospette per motivo sospetto
        pipeline_query_1 = [
            {
                '$match': {
                    'transaction_type': 'deposito'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_count': {'$sum': 1}
                }
            }
        ]

        # Query 2: Importo totale delle transazioni per tipo di transazione
        pipeline_query_2 = [
            {
                '$match': {
                    'transaction_type': 'deposito',
                    'Importo': {'$gt': 8000}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_amount': {'$sum': '$Importo'}
                }
            }
        ]

        # Query 3: Numero di destinatari con importo da transazioni con tipo di pagamento trasferimento
        pipeline_query_3 = [
            {
                '$match': {
                    'transaction_type': 'deposito',
                    'Importo': {'$gt': 8000}
                }
            },
            {
                '$lookup': {
                    'from': collection_names[percentage]['destinatari'],  # Usa la percentuale corretta
                    'localField': 'receiver_id',
                    'foreignField': 'receiver_id',
                    'as': 'destinatari_data'
                }
            },
            {
                '$match': {
                    'destinatari_data.Nationality': 'Sweden'
                }
            },
            {
                '$count': 'total_count'
            }
        ]

        # Query 4: Conta il numero di transazioni con tipo di pagamento 'pagamento' e importo maggiore di 9000,
        # o con data di transazione che contiene '2023-08'.
        pipeline_query_4 = [
            {
                '$match': {
                    '$or': [
                        {'transaction_type': 'pagamento', 'Importo': {'$gt': 9000}},
                        {'transaction_date': {'$regex': '2023-08-07'}}
                    ]
                }
            },
            {
                '$lookup': {
                    'from': collection_names[percentage]['mittenti'],
                    'localField': 'sender_id',
                    'foreignField': 'sender_id',
                    'as': 'mittenti_data'
                }
            },
            {
                '$match': {
                    'mittenti_data.Nationality': 'Seychelles'
                }
            },
            {
                '$lookup': {
                    'from': collection_names[percentage]['destinatari'],
                    'localField': 'receiver_id',
                    'foreignField': 'receiver_id',
                    'as': 'destinatari_data'
                }
            },
            {
                '$match': {
                    'destinatari_data.Nationality': 'Puerto Rico'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_count': {'$sum': 1}
                }}
        ]

        # Lista delle query
        queries = {
            'Query 1': pipeline_query_1,
            'Query 2': pipeline_query_2,
            'Query 3': pipeline_query_3,
            'Query 4': pipeline_query_4
        }

        # Funzione per eseguire la query
        def execute_query(collection, pipeline):
            def wrapper():
                result = list(collection.aggregate(pipeline))  # Utilizza aggregate con la pipeline
                return result

            return wrapper


        # Esecuzione degli esperimenti e registrazione dei risultati nel file CSV
        for query_name, pipeline in queries.items():
            print(f"  Esecuzione Query: {query_name}")

            single_query_times = []  # Per memorizzare i tempi delle 30 esecuzioni successive
            first_execution_time = 0  # Per memorizzare il tempo della prima esecuzione

            for i in range(num_executions):
                print('Esecuzione num: ', i)
                query_func = execute_query(db[collection_names[percentage]['transazioni']], pipeline)
                start_time = time.perf_counter()
                result = query_func()  # Esecuzione effettiva della query
                elapsed_time = (time.perf_counter() - start_time) * 1000  # Tempo in millisecondi

                if i == 0:
                    first_execution_time = elapsed_time
                else:
                    single_query_times.append(elapsed_time)

            # Calcola il tempo medio basato sulle 30 esecuzioni successive
            avg_time = statistics.mean(single_query_times) if single_query_times else 0
            confidence_interval = scipy.stats.t.interval(0.95, len(single_query_times) - 1, loc=avg_time,
                                                         scale=scipy.stats.sem(single_query_times))

            # Scrittura dei risultati nel file CSV
            csvwriter.writerow([query_name, f'{percentage}', first_execution_time, avg_time,
                                f'({confidence_interval[0]}, {confidence_interval[1]})'])

            print(f"    Prima Esecuzione: {first_execution_time:.2f} ms")
            print(f"    Media Esecuzioni Successive: {avg_time:.2f} ms")
            print(f"  Intervallo di confidenza: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")

# Chiusura del file CSV
csvfile.close()

# Chiusura della connessione a MongoDB
client.close()
