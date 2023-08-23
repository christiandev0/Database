import csv
from pymongo import MongoClient
import timeit
import statistics
import matplotlib.pyplot as plt
import openpyxl
import scipy.stats
import queries  # Importa le query definite nel file queries.py

#Connessione a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Antiriciclaggio']  # Cambia il nome del database se necessario

# Definizione delle collezioni
mongo_collection_25 = mongo_db['Db_25']
mongo_collection_50 = mongo_db['Db_50']
mongo_collection_75 = mongo_db['Db_75']
mongo_collection_100 = mongo_db['Db_100']

# Definizione dei dataset
mongo_collections = {
    '25%': mongo_collection_25,
    '50%': mongo_collection_50,
    '75%': mongo_collection_75,
    '100%': mongo_collection_100
}

# Numero di esecuzioni per ogni query e dataset
num_executions = 31

# Foglio elettronico per i risultati
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(['Query', 'Percentuale Dati', 'Esecuzione', 'Tempo (ms)', 'Intervallo Inf (ms)', 'Intervallo Sup (ms)'])

# Funzione per eseguire la query e misurare il tempo utilizzando timeit
# Funzione per eseguire la query e misurare il tempo utilizzando timeit
def execute_query(collection, query):
    def wrapper():
        result = list(collection.find(query))  # Converti il risultato in una lista
    return wrapper

with open('Risultati_esperimenti.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Query', 'Percentuale Dati', 'Esecuzione', 'Tempo (ms)', 'Intervallo Inf (ms)', 'Intervallo Sup (ms)'])

    # Esegui gli esperimenti e registra i risultati nel file CSV
    for query_name, query_list in queries.queries.items():
        first_execution_times = []  # Lista per i tempi della prima esecuzione
        query_avg_times = []  # Lista per i tempi medi delle esecuzioni successive (reset per ogni query)
        confidence_intervals = []  # Lista per gli intervalli di confidenza
        for dataset_percentage, collection in mongo_collections.items():
            print(f"Query: {query_name}, Dataset: {dataset_percentage}")
            single_query_times = []
            for _ in range(num_executions):
                query_func = execute_query(collection, query_list[0])
                start_time = timeit.timeit(query_func, number=1)
                elapsed_time = start_time * 1000  # Tempo in millisecondi
                single_query_times.append(elapsed_time)
                if _ == 0:
                    first_execution_times.append(elapsed_time)  # Aggiungi il tempo della prima esecuzione

            avg_time = statistics.mean(single_query_times)
            confidence_interval = scipy.stats.t.interval(0.95, len(single_query_times) - 1, loc=avg_time,
                                                         scale=scipy.stats.sem(single_query_times))
            query_avg_times.append(avg_time)
            confidence_intervals.append((confidence_interval[1] - confidence_interval[
                0]) / 2)  # L'intervallo completo è troppo grande per visualizzarlo in barre dell'errore

            # Aggiungi i tempi delle prime esecuzioni al file CSV
            csvwriter.writerow([query_name, dataset_percentage, 'First Execution Time', '', '', first_execution_times[0]])

            # Aggiungi i tempi medi e gli intervalli di confidenza al file CSV
            csvwriter.writerow([query_name, dataset_percentage, 'Avg Time', '', '', avg_time])
            csvwriter.writerow([query_name, dataset_percentage, 'Confidence Interval', '', confidence_interval[0], confidence_interval[1]])

            print(f"  Tempo medio: {avg_time:.2f} ms")
            print(f"  Intervallo di confidenza: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")

        # Crea un istogramma per il tempo della prima esecuzione
        plt.figure()
        plt.bar([str(p) for p in mongo_collections.keys()], first_execution_times, color='blue', alpha=0.7)
        plt.xlabel('Percentuale Dataset')
        plt.ylabel('Tempo (ms)')
        plt.title(f'Istogramma Prima Esecuzione - Query {query_name}')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.savefig(f'hist_first_execution_{query_name}.png')
        plt.close()

        # Crea un istogramma per il tempo medio delle successive 30 esecuzioni
        plt.figure()
        plt.bar([str(p) for p in mongo_collections.keys()], query_avg_times, color='blue', alpha=0.7, yerr=confidence_intervals, capsize=5)
        plt.xlabel('Percentuale Dataset')
        plt.ylabel('Tempo Medio (ms)')
        plt.title(f'Istogramma Tempo Medio 30 Esecuzioni - Query {query_name}')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.savefig(f'hist_avg_30_executions_{query_name}.png')
        plt.close()

# Chiudi il file CSV
csvfile.close()

# Chiudi la connessione
mongo_client.close()
