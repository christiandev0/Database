from neo4j import GraphDatabase
import csv

# Connessione al database Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Antiriciclaggio"
driver100 = GraphDatabase.driver(uri, auth=(username, password), database="db100")
driver75 = GraphDatabase.driver(uri, auth=(username, password), database="db75")
driver50 = GraphDatabase.driver(uri, auth=(username, password), database="db50")
driver25 = GraphDatabase.driver(uri, auth=(username, password), database="db25")

# Lettura dei dati dal file CSV
transactions_data = []
with open('transactions.csv', 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        transactions_data.append(row)


# Funzione per inserire i dati da un dataset nel database Neo4j
def insert_data_to_neo4j(dataset, session):
    query = """
    UNWIND $rows as row
    MERGE (mitt:Mittente {nome: row.Mittente})
    MERGE (dest:Destinatario {nome: row.Destinatario})
    CREATE (mitt)-[:TRANS{importo: row.Importo, data: row.Data}]->(dest)
    """
    session.run(query, rows=dataset)


# Dividi i dati in dataset corrispondenti
db25 = transactions_data[:int(len(transactions_data) * 0.25)]
db50 = transactions_data[:int(len(transactions_data) * 0.50)]
db75 = transactions_data[:int(len(transactions_data) * 0.75)]
db100 = transactions_data

# Inserisci i dati nei diversi database di Neo4j
with driver25.session() as session:
    insert_data_to_neo4j(db25, session)
    print("Inserimento nel dataset 25% completato")

with driver50.session() as session:
    insert_data_to_neo4j(db50, session)
    print("Inserimento nel dataset 50% completato")

with driver75.session() as session:
    insert_data_to_neo4j(db75, session)
    print("Inserimento nel dataset 75% completato")

with driver100.session() as session:
    database_name = "db100"
    insert_data_to_neo4j(db100, session)
    print("Inserimento nel dataset 100% completato")

# Chiudi la connessione al database Neo4j
driver25.close()
driver50.close()
driver75.close()
driver100.close()
