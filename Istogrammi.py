import csv
from audioop import avg

import matplotlib.pyplot as plt


# Leggi i dati dai file CSV
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Salta l'intestazione
        for row in csv_reader:
            data.append(row)
    return data


# File CSV con i dati di MongoDB
mongodb_csv = 'Risultati_esperimenti_MongoDB.csv'
mongodb_data = read_csv_file(mongodb_csv)

# File CSV con i dati di Neo4j
neo4j_csv = 'Risultati_esperimenti_Neo4j.csv'
neo4j_data = read_csv_file(neo4j_csv)

# Estrai i dati necessari
queries = []
percentages = []
first_execution_times_mongodb = []
avg_execution_times_mongodb = []
confidence_intervals_mongodb = []
first_execution_times_neo4j = []
avg_execution_times_neo4j = []
confidence_intervals_neo4j = []

for row in mongodb_data:
    query = row[0]
    percentage = row[1]
    if row[2] == 'First Execution Time':
        queries.append(query)
        percentages.append(percentage)
        first_execution_times_mongodb.append(float(row[5]))
        print("Adding to first_execution_times_mongodb")
        print(first_execution_times_mongodb)
    elif row[2] == 'Avg Time':
        avg_execution_times_mongodb.append(float(row[5]))
    elif row[2] == 'Confidence Interval':
        confidence_intervals_mongodb.append(float(row[5]))

for row in neo4j_data:
    query = row[0]
    percentage = row[1]
    if row[2] == 'First Execution Time (ms)':
        first_execution_times_neo4j.append(float(row[3]))
    elif row[2] == 'Average Execution Time (ms)':
        avg_execution_times_neo4j.append(float(row[3]))
    elif row[2] == 'Confidence Interval (95%)':
        confidence_interval = row[3].strip("()").split(", ")
        confidence_intervals_neo4j.append((float(confidence_interval[0]), float(confidence_interval[1])))


# Crea gli istogrammi
x = range(len(queries))

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(x, first_execution_times_mongodb, width=0.4, label='MongoDB')
plt.bar([i + 0.4 for i in x], first_execution_times_neo4j, width=0.4, label='Neo4j')
plt.xlabel('Query')
plt.ylabel('Tempo di esecuzione (ms)')
plt.title('Tempi delle Prime Esecuzioni')
plt.xticks([i + 0.2 for i in x], queries, rotation=45, ha='right')
plt.legend()

plt.subplot(1, 2, 2)
plt.bar(x, avg_execution_times_mongodb, yerr=confidence_intervals_mongodb, width=0.4, label='MongoDB')
plt.bar([i + 0.4 for i in x], avg_execution_times_neo4j, yerr=[(ci[0] - avg, ci[1] - avg) for ci in confidence_intervals_neo4j], width=0.4, label='Neo4j')
plt.xlabel('Query')
plt.ylabel('Tempo di esecuzione medio (ms)')
plt.title('Tempi Medi con Intervalli di Confidenza al 95%')
plt.xticks([i + 0.2 for i in x], queries, rotation=45, ha='right')
plt.legend()

plt.tight_layout()
plt.show()
