import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_mongo = pd.read_csv('Risultati_esperimenti_MongoDB.csv')
data_neo4j = pd.read_csv('Risultati_esperimenti_Neo4j.csv')

dataset_sizes = ['100%', '75%', '50%', '25%']
queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4']

bar_width = 0.4  # Larghezza delle barre
bar_positions = np.arange(len(dataset_sizes))

for query in queries:
    plt.figure(figsize=(12, 6))

    for i, size in enumerate(dataset_sizes):
        data_mongo_query = data_mongo[(data_mongo['Query'] == query) & (data_mongo['Database'] == size)]
        data_neo4j_query = data_neo4j[(data_neo4j['Query'] == query) & (data_neo4j['Database'] == size)]

        values_mongo_first = float(data_mongo_query['First Execution Time (ms)'].values[0])
        values_neo4j_first = float(data_neo4j_query['First Execution Time (ms)'].values[0])

        plt.bar(bar_positions[i] - bar_width / 2, values_mongo_first, width=bar_width, align='center', color='b',
                alpha=0.5, label='MongoDB - First Execution')
        plt.bar(bar_positions[i] + bar_width / 2, values_neo4j_first, width=bar_width, align='center', color='r',
                alpha=0.5, label='Neo4j - First Execution')

    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di prima esecuzione (ms)')
    plt.title(f'Istogramma - Tempi della Prima Esecuzione per {query}')
    plt.xticks(bar_positions, dataset_sizes)
    plt.ylim(0, max(data_mongo['First Execution Time (ms)']) * 1.1)  # Imposta l'intervallo sull'asse y
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))

    for i, size in enumerate(dataset_sizes):
        data_mongo_query = data_mongo[(data_mongo['Query'] == query) & (data_mongo['Database'] == size)]
        data_neo4j_query = data_neo4j[(data_neo4j['Query'] == query) & (data_neo4j['Database'] == size)]

        values_mongo_avg = float(data_mongo_query['Average Execution Time (ms)'].values[0])
        values_neo4j_avg = float(data_neo4j_query['Average Execution Time (ms)'].values[0])

        plt.bar(bar_positions[i] - bar_width / 2, values_mongo_avg, width=bar_width, align='center', color='b',
                alpha=0.5, label='MongoDB - Avg Execution')
        plt.bar(bar_positions[i] + bar_width / 2, values_neo4j_avg, width=bar_width, align='center', color='r',
                alpha=0.5, label='Neo4j - Avg Execution')

    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione medio (ms)')
    plt.title(f'Istogramma - Tempi Medi di Esecuzione per {query}')
    plt.xticks(bar_positions, dataset_sizes)
    plt.legend()
    plt.tight_layout()
    plt.show()
