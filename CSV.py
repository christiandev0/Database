import csv
from faker import Faker
import random

fake = Faker()
csv_file_path = 'C:/Users/Christian.DESKTOP-0MQUKSN/PycharmProjects/pythonProject/ProgettoDB'
transactions_data = []

print("Lista di nomi sospetti salvata con successo in:", csv_file_path)

for _ in range(10000):
    mittente = fake.name()
    destinatario = fake.name()
    paese_cliente = fake.random_element(elements=('Italia', 'Francia', 'Germania', 'Stati Uniti', 'Giappone',
                                                  'Russia', 'Colombia', 'Regno Unito', 'Canada'))
    transaction = {
        'id': fake.uuid4(),
        'Mittente': mittente,
        'Destinatario': destinatario,
        'Importo': fake.random_int(min=1, max=10000),
        'Data': fake.date_time_this_year(),
        'Metodo_di_pagamento': fake.random_element(elements=('Bonifico', 'Carta di credito', 'PayPal', 'Assegno')),
        'Valuta': fake.random_element(elements=('EUR', 'USD', 'GBP', 'JPY')),
        'Paese_del_Cliente': paese_cliente,
        'Paese_a_Rischio': 'Si' if paese_cliente not in ['Italia', 'Francia', 'Germania'] else 'No',
        'Mittente_sospetto': random.choice(['Si', 'No']),
        'Destinatario_sospetto': random.choice(['Si', 'No'])
    }
    transactions_data.append(transaction)

csv_file_path = 'transactions.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['id', 'Mittente', 'Destinatario', 'Importo', 'Data', 'Metodo_di_pagamento', 'Valuta',
                  'Paese_del_Cliente', 'Paese_a_Rischio', 'Mittente_sospetto', 'Destinatario_sospetto']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(transactions_data)


print("File CSV creato con successo:", csv_file_path)
