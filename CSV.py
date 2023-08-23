import csv
from faker import Faker

fake = Faker()
csv_file_path = 'C:/Users/Christian.DESKTOP-0MQUKSN/PycharmProjects/pythonProject/ProgettoDB'
transactions_data = []
for _ in range(10000):
    transaction = {
        'id': fake.uuid4(),
        'Mittente': fake.name(),
        'Destinatario': fake.name(),
        'Importo': fake.random_int(min=1, max=1000),
        'Data': fake.date_time_this_year()
    }
    transactions_data.append(transaction)

csv_file_path = 'transactions.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['id', 'Mittente', 'Destinatario', 'Importo', 'Data']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(transactions_data)

print("File CSV creato con successo: ", csv_file_path)