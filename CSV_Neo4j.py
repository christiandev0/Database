import csv
import statistics
from scipy.stats import t
import time
from neo4j import GraphDatabase

# Definisci le query
queries = [
    """
    MATCH (n:Transazione)
    WHERE n.Importo > 1000
    OR (n.Mittente = 'MittenteSospetto' AND n.Destinatario = 'DestinatarioSospetto')
    OR (n.Importo > 500 OR n.Mittente = 'MittenteSospetto' OR n.Destinatario = 'DestinatarioSospetto')
    OR (n.Importo > 1000 AND n.Mittente = 'MittenteSospetto' AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
    RETURN n

    """,
    """
    MATCH (n:Transazione)
WHERE n.Importo > 1000
OR (n.Mittente = 'MittenteSospetto' AND n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 500 OR n.Mittente = 'MittenteSospetto' OR n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 1000 AND n.Mittente = 'MittenteSospetto' AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
RETURN n

    """,
    """
    MATCH (n:Transazione)
WHERE n.Importo > 1000
OR (n.Mittente = 'MittenteSospetto' AND n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 500 OR n.Mittente = 'MittenteSospetto' OR n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 1000 AND n.Mittente = 'MittenteSospetto' AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
RETURN n

    """,
    """
    MATCH (n:Transazione)
WHERE n.Importo > 1000
OR (n.Mittente = 'MittenteSospetto' AND n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 500 OR n.Mittente = 'MittenteSospetto' OR n.Destinatario = 'DestinatarioSospetto')
OR (n.Importo > 1000 AND n.Mittente = 'MittenteSospetto' AND n.Data >= '2023-01-01T00:00:00Z' AND n.Data <= '2023-12-31T23:59:59Z')
RETURN n
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
        print(f"Esecuzione Query {query_idx + 1}  {percentage}")
        execution_times_query = []

        with driver.session() as session:
            for _ in range(num_executions):
                start_time = time.time()
                # Esegui la query e ottieni il risultato
                result = session.run(query).data()
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                execution_times_query.append(execution_time)

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

# Scrivi i risultati nel file CSV
csv_file = 'Risultati_esperimenti_Neo4j.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Database', 'First Execution Time (ms)', 'Average Execution Time (ms)',
                  'Confidence Interval (95%)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)

# Chiudi la connessione al database Neo4j
driver.close()
