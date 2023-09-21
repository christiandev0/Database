import csv
import statistics
import time
from neo4j import GraphDatabase


# Funzione per l'esecuzione delle query in Neo4j
def execute_query(tx, query):
    result = list(tx.run(query))  # Esegui la query
    return result


# Connessione a Neo4j
uri = "bolt://localhost:7687"  # Cambia l'URI in base alla tua configurazione
username = "neo4j"
password = "Antiriciclaggio"

# Lista delle percentuali da iterare
percentages = ['100%', '75%', '50%', '25%']

# Definizione delle query per Neo4j
queries_neo4j = {
    'Query 1': (
        f"MATCH (t:transazioni) "
        f"WHERE t.transaction_type = 'deposito' "
        f"RETURN count(t) as total_count"
    ),
    'Query 2': (
        f"MATCH (t:transazioni) "
        f"WHERE t.transaction_type = 'deposito' AND t.Importo > 8000 "
        f"RETURN sum(t.Importo) as total_amount"
    ),
    'Query 3': (
        f"MATCH (t:transazioni)-[:RICEVE]->(d:destinatari) "
        f"WHERE t.transaction_type = 'deposito' AND t.Importo > 8000 AND d.Nationality = 'Sweden' "
        f"RETURN count(d) as total_count"
    ),
    'Query 4': (
        f"MATCH (t:transazioni) "
        f"WHERE (t.transaction_type = 'pagamento' AND t.Importo > 9000) "
        f"MATCH (s:mittenti)-[:EFFETTUA]->(t) "
        f"WHERE s.Nationality = 'Seychelles' "
        f"MATCH (t)-[:RICEVE]->(d:destinatari) "
        f"WHERE d.Nationality = 'Puerto Rico' "
        f"RETURN count(t) as total_count"
    )
}

# Nome del file CSV
csv_filename = 'Risultati_esperimenti_Neo4j.csv'

# Numero di esecuzioni per ogni query
num_executions = 31

# Apertura del file CSV per la scrittura
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        ['Query', 'Dataset', 'Prima Esecuzione (ms)', 'Media Esecuzioni Successive (ms)', 'Confidence Interval (95%)'])

    for percentage in percentages:
        database_name = f"antiriciclaggio{percentage[:-1]}"  # Rimuove il simbolo '%' per ottenere il nome del database
        driver = GraphDatabase.driver(uri, auth=(username, password), database=database_name)
        print(f"Analisi per la percentuale: {percentage}")

        # Esegue ogni query
        for query_name, query_text in queries_neo4j.items():
            print(f"Esecuzione Query: {query_name}")

            single_query_times = []  # Per memorizzare i tempi delle 30 esecuzioni successive
            first_execution_time = 0  # Per memorizzare il tempo della prima esecuzione

            # Esegue la query 31 volte
            for i in range(num_executions):
                with driver.session() as session:
                    start_time = time.perf_counter()
                    result = session.execute_write(execute_query, query_text)
                    print(result)
                    elapsed_time = (time.perf_counter() - start_time) * 1000  # Tempo in millisecondi

                    if i == 0:
                        first_execution_time = elapsed_time
                    else:
                        single_query_times.append(elapsed_time)

                print(result)

            # Calcola il tempo medio basato sulle 30 esecuzioni successive
            avg_time = statistics.mean(single_query_times) if single_query_times else 0
            confidence_interval = statistics.stdev(single_query_times) * 1.96 / (num_executions ** 0.5)

            # Scrittura dei risultati nel file CSV
            csvwriter.writerow([query_name, f'{percentage}', first_execution_time, avg_time,
                                f'({avg_time - confidence_interval:.2f}, {avg_time + confidence_interval:.2f})'])

            print(f"  Prima Esecuzione: {first_execution_time:.2f} ms")
            print(f"  Media Esecuzioni Successive: {avg_time:.2f} ms")
            print(
                f"  Intervallo di confidenza: ({avg_time - confidence_interval:.2f}, {avg_time + confidence_interval:.2f})")

# Chiusura della connessione a Neo4j
driver.close()
