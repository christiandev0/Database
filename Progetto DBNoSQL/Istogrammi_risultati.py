import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.patches import Patch

# Carica i dati dai file CSV
data_mongo = pd.read_csv('Risultati_esperimenti_MongoDB.csv')
data_neo4j = pd.read_csv('Risultati_esperimenti_Neo4j.csv')

# Lista delle dimensioni del dataset
dataset_sizes = ['100%', '75%', '50%', '25%']

# Lista delle query
queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4']


# Funzione per estrarre i valori minimi e massimi dell'intervallo di confidenza
def extract_confidence_values(confidence_interval_str):
    matches = re.findall(r'\d+\.\d+', confidence_interval_str)
    return float(matches[0]), float(matches[1])


# Per ogni query crea gli istogrammi
for query in queries:
    # Filtra i dati per la query corrente
    data_mongo_query = data_mongo[data_mongo['Query'] == query]
    data_neo4j_query = data_neo4j[data_neo4j['Query'] == query]

    # Creazione del primo istogramma con i tempi della prima esecuzione
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo = data_mongo_query[data_mongo_query['Dataset'] == size]['Prima Esecuzione (ms)']
        values_neo4j = data_neo4j_query[data_neo4j_query['Dataset'] == size]['Prima Esecuzione (ms)']

        plt.bar([f"{size} (MongoDB)", f"{size} (Neo4j)"], [values_mongo.values[0], values_neo4j.values[0]],
                color=['blue', 'magenta'])

    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione (ms)')
    plt.title(f'Istogramma - Tempo della Prima Esecuzione per {query}')
    legend_elements = [Patch(facecolor='blue', label='MongoDB'), Patch(facecolor='magenta', label='Neo4j')]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.show()

    # Creazione del secondo istogramma con le medie dei tempi e gli intervalli
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo = data_mongo_query[data_mongo_query['Dataset'] == size]['Media Esecuzioni Successive (ms)']
        values_neo4j = data_neo4j_query[data_neo4j_query['Dataset'] == size]['Media Esecuzioni Successive (ms)']

        # Estrazione intervalli di confidenza
        confidence_intervals_mongo = data_mongo_query[data_mongo_query['Dataset'] == size][
            'Confidence Interval (95%)']
        confidence_intervals_neo4j = data_neo4j_query[data_neo4j_query['Dataset'] == size][
            'Confidence Interval (95%)']
        conf_intervals_mongo = [extract_confidence_values(conf_str) for conf_str in confidence_intervals_mongo]
        conf_intervals_neo4j = [extract_confidence_values(conf_str) for conf_str in confidence_intervals_neo4j]

        # Estrazione valori minimi e massimi dagli intervalli di confidenza
        conf_mongo_min = [conf[0] for conf in conf_intervals_mongo]
        conf_mongo_max = [conf[1] for conf in conf_intervals_mongo]
        conf_neo4j_min = [conf[0] for conf in conf_intervals_neo4j]
        conf_neo4j_max = [conf[1] for conf in conf_intervals_neo4j]

        plt.bar([f"{size} (MongoDB)", f"{size} (Neo4j)"], [values_mongo.values[0], values_neo4j.values[0]],
                color=['blue', 'red'])
        plt.errorbar([f"{size} (MongoDB)", f"{size} (Neo4j)"], [values_mongo.values[0], values_neo4j.values[0]],
                     yerr=[[values_mongo.values[0] - conf_mongo_min[0], conf_mongo_max[0] - values_mongo.values[0]],
                           [values_neo4j.values[0] - conf_neo4j_min[0], conf_neo4j_max[0] - values_neo4j.values[0]]],
                     capsize=5, fmt='none')

    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione medio (ms)')
    plt.title(f'Istogramma - Tempo di Esecuzione Medio per {query}')
    legend_elements = [Patch(facecolor='blue', label='MongoDB'), Patch(facecolor='red', label='Neo4j')]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.show()
