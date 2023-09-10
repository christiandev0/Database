import csv
import time
from neo4j import GraphDatabase
import numpy as np
from scipy.stats import t

# Definizione delle query
queries = [
    """ 
    MATCH (t:Transazione)
    WHERE t.Importo < '1000'
    RETURN t
    """,
    """ 
    MATCH (t:Transazione)
    WHERE t.Importo > '2000'
    OR (t.Paese_a_Rischio = 'Sì'
    AND t.Metodo_di_pagamento = 'Bonifico'
    AND t.Data < '2023-06-30T00:00:00Z')
    RETURN t
    """,
    """ 
    MATCH (t:Transazione)
    WHERE (t.Paese_a_Rischio = 'Si' AND t.Importo > '1500')
    OR (t.Paese_a_Rischio = 'No' AND t.Metodo_di_pagamento <> 'PayPal')
    AND t.Data >= '2023-01-01T00:00:00Z' AND t.Data <= '2023-12-31T23:59:59Z'
    RETURN t
    """,
    """ 
    MATCH (t:Transazione)-[:DESTINATO_A]->(d:Destinatario)
    WHERE (t.Paese_a_Rischio = 'Si' AND t.Importo > '1500' AND t.Metodo_di_pagamento = 'Assegno') OR
    (t.Mittente_sospetto = 'Si' OR t.Destinatario_sospetto = 'Si' AND t.Importo > '500')
    AND t.Data > '2023-09-15T00:00:00Z'
    RETURN t, d
    """
]
# Definizione delle percentuali
percentages = ['25%', '50%', '75%', '100%']
num_executions = 31
# Connessione al database Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Antiriciclaggio"

# Lista per memorizzare i tempi di esecuzione
execution_times = []

# Ciclo sui database e sulle query
for db_percentage in percentages:
    database_name = f"db{db_percentage[:-1]}"  # Rimuovi il simbolo '%' per ottenere il nome del database
    driver = GraphDatabase.driver(uri, auth=(username, password), database=database_name)

    for query_idx, query in enumerate(queries):
        print(f"Esecuzione Query {query_idx + 1}  {db_percentage}")
        execution_times_query = []
        ignore_first_execution = True  # Variabile per ignorare la prima esecuzione della prima query al 25%
        first_execution_time = None
        with driver.session() as session:
            for _ in range(num_executions):
                start_time = time.perf_counter()
                # Esegui la query e ottieni il risultato
                result = session.run(query).data()
                execution_time = (time.perf_counter() - start_time) * 1000
                execution_times_query.append(execution_time)
                # Ignora la prima esecuzione della prima query al 25%
                if query_idx == 0 and first_execution_time is None:
                    first_execution_time = execution_time

            avg_execution_time = np.mean(execution_times_query)
            std_deviation = np.std(execution_times_query)
            confidence_interval = t.interval(0.95, num_executions - 1, loc=avg_execution_time,
                                             scale=std_deviation / np.sqrt(num_executions - 1))
            print(f"Tempo di esecuzione medio (ms): {avg_execution_time}")
            print(f"Tempo della prima esecuzione (ms): {first_execution_time}")
            print(f"Intervallo di confidenza al 95%: {confidence_interval}")

            execution_times.append({
                "Query": f"Query {query_idx + 1}",
                "Database": f'{db_percentage}',
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
