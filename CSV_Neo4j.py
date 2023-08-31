import csv
import statistics

import scipy
from scipy.stats import t
import time
from neo4j import GraphDatabase

# Definizione delle query
queries = [
    """MATCH (n:Transazione)
       WHERE n.Importo > 1000 OR
             (n.Mittente IN ['MittenteSospetto'] AND n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 500 OR n.Mittente IN ['MittenteSospetto'] OR n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 1000 AND n.Mittente IN ['MittenteSospetto'] AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
       RETURN n
    """,
    """MATCH (n:Transazione)
       WHERE n.Importo > 1000 OR
             (n.Mittente IN ['MittenteSospetto'] AND n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 500 OR n.Mittente IN ['MittenteSospetto'] OR n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 1000 AND n.Mittente IN ['MittenteSospetto'] AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
       RETURN n
    """,
    """MATCH (n:Transazione)
       WHERE n.Importo > 1000 OR
             (n.Mittente IN ['MittenteSospetto'] AND n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 500 OR n.Mittente IN ['MittenteSospetto'] OR n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 1000 AND n.Mittente IN ['MittenteSospetto'] AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
       RETURN n
    """,
    """MATCH (n:Transazione)
       WHERE n.Importo > 1000 OR
             (n.Mittente IN ['MittenteSospetto'] AND n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 500 OR n.Mittente IN ['MittenteSospetto'] OR n.Destinatario IN ['DestinatarioSospetto']) OR
             (n.Importo > 1000 AND n.Mittente IN ['MittenteSospetto'] AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
       RETURN n
    """
]

# Definizione delle percentuali
percentages = ['25%', '50%', '75%', '100%']
num_executions = 31
# Connessione al database Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Antiriciclaggio"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lista per memorizzare i tempi di esecuzione
execution_times = []

# Esecuzione delle query per diverse percentuali
for query_idx, query in enumerate(queries):
    for percentage in percentages:
        print(f"Esecuzione Query {query_idx + 1}  {percentage}")
        execution_times_query = []
        ignore_first_execution = True  # Variabile per ignorare la prima esecuzione della prima query al 25%
        with driver.session() as session:
            for _ in range(num_executions):
                start_time = time.perf_counter()
                # Esegui la query e ottieni il risultato
                result = session.run(query).data()
                execution_time = (time.perf_counter() - start_time) * 1000
                # Ignora la prima esecuzione della prima query al 25%
                if query_idx == 0 and percentage == '25%' and ignore_first_execution:
                    ignore_first_execution = False
                    continue
                execution_times_query.append(execution_time)
            avg_execution_time = statistics.mean(execution_times_query)  # Calcola la media
            first_execution_time = execution_times_query[0]
            confidence_interval = scipy.stats.t.interval(0.95, len(execution_times_query) - 1, loc=avg_execution_time,
                                                         scale=scipy.stats.sem(execution_times_query))

            print(f"Tempo di esecuzione medio (ms): {avg_execution_time}")
            print(f"Tempo della prima esecuzione (ms): {first_execution_time}")
            print(f"Intervallo di confidenza al 95%: {confidence_interval}")

            execution_times.append({
                "Query": f"Query {query_idx + 1}",
                "Database": f'{percentage}',
                "First Execution Time (ms)": first_execution_time,
                "Average Execution Time (ms)": avg_execution_time,
                "Confidence Interval (95%)": confidence_interval,
            })

# Scrittura dei risultati nel file CSV
csv_file = 'Risultati_esperimenti_Neo4j.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Database', 'First Execution Time (ms)', 'Average Execution Time (ms)',
                  'Confidence Interval (95%)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)

# Chiusura della connessione al database Neo4j
driver.close()
