import pandas as pd
from py2neo import Graph, Node, Relationship

Db100 = Graph("bolt://localhost:7687", user="neo4j", password="Antiriciclaggio", name="antiriciclaggio100")
Db75 = Graph("bolt://localhost:7687", user="neo4j", password="Antiriciclaggio", name="antiriciclaggio75")
Db50 = Graph("bolt://localhost:7687", user="neo4j", password="Antiriciclaggio", name="antiriciclaggio50")
Db25 = Graph("bolt://localhost:7687", user="neo4j", password="Antiriciclaggio", name="antiriciclaggio25")

# Dizionario per mappare le percentuali ai grafi
percentuali_Db = {
    25: Db25,
    50: Db50,
    75: Db75,
    100: Db100
}

# Tipi di dati
entities = ['mittenti', 'destinatari', 'transazioni']

for data_type in entities:
    for percentage in percentuali_Db:
        csv_filename = f'{data_type}_{percentage}%.csv'

        # Leggi il file dal CSV
        data = pd.read_csv(csv_filename)

        # Converti i dati in una lista di dizionari
        data_dict_list = data.to_dict(orient='records')

        # Ottiene il grafo corrispondente alla percentuale
        graph = percentuali_Db[percentage]

        # Inserisce i dati nel grafo
        for index, row in data.iterrows():
            node = Node(data_type, **row.to_dict())
            graph.create(node)

            if data_type == 'transazioni':
                # Crea relazione con utente
                nodo_mittente = graph.nodes.match('mittenti', sender_id=row['sender_id']).first()
                if nodo_mittente:
                    transazione_del_mittente = Relationship(nodo_mittente, 'EFFETTUA', node)
                    graph.create(transazione_del_mittente)
                # Crea relazione con destinatario
                nodo_destinatario = graph.nodes.match('destinatari', receiver_id=row['receiver_id']).first()
                if nodo_destinatario:
                    transazione_al_destinatario = Relationship(node, 'RICEVE', nodo_destinatario)
                    graph.create(transazione_al_destinatario)

        print(f"Dati del dataset {data_type}_{percentage}% inseriti in Neo4j con successo.")

print("Inserimento completato per tutti i dataset."
      )
