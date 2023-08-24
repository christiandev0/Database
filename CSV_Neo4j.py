import csv
import statistics
from scipy.stats import t
import time
from neo4j import GraphDatabase

# Definisci le query
queries = [
    """
    MATCH (n:Mittente)
    RETURN COUNT(n) AS total_mittenti
    """,
    """
    MATCH (n:Destinatario)
    RETURN COUNT(n) AS total_destinatari
    """,
    """
    MATCH (n:Mittente)-[r:TRANS]->(d:Destinatario)
    RETURN COUNT(r) AS total_transazioni
    """,
    """
    MATCH (n:Mittente)-[r:TRANS]->(d:Destinatario)
    RETURN AVG(toFloat(r.importo)) AS avg_importo
    """
]

# Definisci le percentuali
percentages = ['25%', '50%', '75%', '100%']
num_executions = 31
# Connessione al database Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Antiriciclaggio"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Lista per memorizzare i tempi di esecuzione
execution_times = []

# Esegui le query per diverse percentuali
for query_idx, query in enumerate(queries):
    for percentage in percentages:
        print(f"Esecuzione Query {query_idx + 1} - {percentage}")
        execution_times_query = []

        with driver.session() as session:
            for _ in range(num_executions):
                start_time = time.perf_counter()

                # Esegui la query e ottieni il risultato
                result = session.run(query).data()
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                execution_times_query.append(execution_time)

                print(f"Risultati query {query_idx + 1}: {result}")  # Stampa dei risultati delle query

            avg_execution_time = sum(execution_times_query) / num_executions  # Calcola la media
            confidence_interval = t.interval(0.95, num_executions - 1, loc=avg_execution_time,
                                             scale=statistics.stdev(execution_times_query))
            first_execution_time = execution_times_query[0]

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

            print("-" * 40)

# Scrivi i risultati nel file CSV
csv_file = 'Risultati_esperimenti_Neo4j.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Scrivi l'intestazione
    csvwriter.writerow(
        ['Query', 'Percentuale Dati', 'Esecuzione', 'Tempo (ms)', 'Intervallo Inf (ms)', 'Intervallo Sup (ms)'])

    # Scrivi i risultati
    for data in execution_times:
        query_name = data["Query"]
        percentage = data["Database"]
        first_execution_time = data["First Execution Time (ms)"]
        avg_execution_time = data["Average Execution Time (ms)"]
        confidence_interval = data["Confidence Interval (95%)"]

        # Scrivi le righe nel formato desiderato
        csvwriter.writerow([query_name, percentage, 'First Execution Time', '', '', first_execution_time])
        csvwriter.writerow([query_name, percentage, 'Avg Time', '', '', avg_execution_time])
        csvwriter.writerow([query_name, percentage, 'Confidence Interval', '', confidence_interval[0], confidence_interval[1]])

# Chiudi la connessione al database Neo4j
driver.close()
