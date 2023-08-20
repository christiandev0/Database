from pymongo import MongoClient
import timeit
import statistics
import matplotlib.pyplot as plt
import openpyxl
import scipy.stats
import queries  # Importa le query definite nel file queries.py

# Connessione a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Antiriciclaggio']  # Cambia il nome del database se necessario

# Definizione delle collezioni
mongo_collection_25 = mongo_db['Db_25']
mongo_collection_50 = mongo_db['Db_50']
mongo_collection_75 = mongo_db['Db_75']
mongo_collection_100 = mongo_db['Db_100']

# Definizione dei dataset
mongo_collections = {
    '25': mongo_collection_25,
    '50': mongo_collection_50,
    '75': mongo_collection_75,
    '100': mongo_collection_100
}

# Numero di esecuzioni per ogni query e dataset
num_executions = 31

# Foglio elettronico per i risultati
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(['Query', 'Percentuale Dati', 'Esecuzione', 'Tempo (ms)'])

# Funzione per eseguire la query e misurare il tempo utilizzando timeit
def execute_query(collection, query):
    def wrapper():
        result = collection.find(query)
    return wrapper

# Esegui gli esperimenti e registra i risultati nel foglio elettronico
for query_name, query_list in queries.queries.items():
    for query_name, query_list in queries.queries.items():
        first_execution_times = []  # Lista per i tempi della prima esecuzione
        dataset_percentages = list(mongo_collections.keys())  # Lista delle percentuali di dataset
        query_avg_times = []  # Lista per i tempi medi delle esecuzioni successive (reset per ogni query)
        confidence_intervals = []
        for dataset_percentage, collection in mongo_collections.items():
            print(f"Query: {query_name}, Dataset: {dataset_percentage}%")
            single_query_times = []
            for _ in range(num_executions):
                start_time = timeit.timeit(execute_query(collection, query_list[0]), number=1)
                elapsed_time = start_time * 1000  # Tempo in millisecondi
                single_query_times.append(elapsed_time)
                sheet.append([query_name, dataset_percentage, _ + 1, elapsed_time])

                if _ == 0:
                    first_execution_times.append(elapsed_time)  # Aggiungi il tempo della prima esecuzione

            avg_time = statistics.mean(single_query_times)
            confidence_interval = scipy.stats.t.interval(0.95, len(single_query_times) - 1, loc=avg_time,
                                                         scale=scipy.stats.sem(single_query_times))
            query_avg_times.append(avg_time)
            confidence_intervals.append((confidence_interval[1] - confidence_interval[
                0]) / 2)  # L'intervallo completo è troppo grande per visualizzarlo in barre dell'errore

            print(f"  Tempo medio: {avg_time:.2f} ms")
            print(f"  Intervallo di confidenza: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")

        # Crea un istogramma per il tempo della prima esecuzione
        plt.figure()
        plt.bar(dataset_percentages, first_execution_times, color='blue', alpha=0.7)
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
        plt.bar(dataset_percentages, query_avg_times, color='blue', alpha=0.7, yerr=confidence_intervals, capsize=5)
        plt.xlabel('Percentuale Dataset')
        plt.ylabel('Tempo Medio (ms)')
        plt.title(f'Istogramma Tempo Medio 30 Esecuzioni - Query {query_name}')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.savefig(f'hist_avg_30_executions_{query_name}.png')
        plt.close()

# Salva il foglio elettronico
workbook.save('risultati_esperimenti.xlsx')

# Chiudi la connessione
mongo_client.close()
