from faker import Faker
import random
import csv

fake = Faker()

# Record del dataset 100% per i mittenti e destinatari
total_entities = 10000

# Percentuali dei dataset rispetto al 100%
percentages = [100, 75, 50, 25]

# Tipologie di transazioni
transaction_types = ['bonifico', 'prelievo', 'deposito', 'trasferimento', 'investimento', 'pagamento']

# Dizionario per tenere traccia degli ID delle transazioni e dei valori per ciascun tipo di transazione
transaction_info = {}

for transaction_type in transaction_types:
    transaction_id = len(transaction_info) + 1  # Incrementa l'ID della transazione
    Importo = round(random.uniform(10, 10000), 2)  # Genera un valore casuale

    # Aggiunge le informazioni della transazione al dizionario
    transaction_info[transaction_type] = {
        'transaction_id': transaction_id,
        'Importo': Importo
    }

# Crea i dati per dataset al 100%
senders_100 = []
receivers_100 = []
transactions_100 = []

for entity_num in range(total_entities):
    sender_id = entity_num + 1
    sender = {
        'sender_id': sender_id,
        'Nome': fake.first_name(),
        'Cognome': fake.last_name(),
        'Nationality': fake.country()
    }
    senders_100.append(sender)

    receiver_id = entity_num + 1
    receiver = {
        'receiver_id': receiver_id,
        'Nome': fake.first_name(),
        'Cognome': fake.last_name(),
        'Nationality': fake.country()
    }
    receivers_100.append(receiver)

    for _ in range(random.randint(1, 5)):  # Genera un numero casuale di transazioni per ciascun mittente
        transaction_type = random.choice(transaction_types)
        transaction_id = fake.uuid4()
        transaction_value = 0  # Inizializza il valore della transazione a 0

        # Trova il valore corrispondente al tipo di transazione
        for t_type, t_info in transaction_info.items():
            if t_type == transaction_type:
                transaction_value = t_info['Importo']
                break

        transaction_date = fake.date_time_this_year()

        transaction = {
            'transaction_id': transaction_id,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'transaction_type': transaction_type,
            'Importo': transaction_value,
            'transaction_date': transaction_date,
        }

        transactions_100.append(transaction)

for percentage in percentages:
    num_records = int(total_entities * (percentage / 100))

    # Seleziona il range di ID da inserire nel dataset corrente
    if percentage == 100:
        selected_senders = senders_100
        selected_receivers = receivers_100
        selected_transactions = transactions_100
    elif percentage == 75:
        selected_senders = senders_100[:7500]
        selected_receivers = receivers_100[:7500]
        selected_transactions = transactions_100[:7500]
    elif percentage == 50:
        selected_senders = senders_100[:5000]
        selected_receivers = receivers_100[:5000]
        selected_transactions = transactions_100[:5000]
    elif percentage == 25:
        selected_senders = senders_100[:2500]
        selected_receivers = receivers_100[:2500]
        selected_transactions = transactions_100[:2500]

    # Ordina gli ID dei mittenti e dei destinatari selezionati per il dataset corrente
    selected_senders = sorted(selected_senders, key=lambda x: x['sender_id'])
    selected_receivers = sorted(selected_receivers, key=lambda x: x['receiver_id'])

    # Apre un file CSV per scrivere i mittenti generati
    senders_csv_filename = f'mittenti_{percentage}%.csv'
    with open(senders_csv_filename, 'w', newline='') as senders_csvfile:
        senders_fieldnames = ['sender_id', 'Nome', 'Cognome', 'Nationality']
        senders_writer = csv.DictWriter(senders_csvfile, fieldnames=senders_fieldnames)
        senders_writer.writeheader()

        for sender in selected_senders:
            senders_writer.writerow(sender)

        print(f"File CSV mittenti {percentage}% generato con successo.")

    # Apre un file CSV per scrivere i destinatari
    receivers_csv_filename = f'destinatari_{percentage}%.csv'
    with open(receivers_csv_filename, 'w', newline='') as receivers_csvfile:
        receivers_fieldnames = ['receiver_id', 'Nome', 'Cognome', 'Nationality']
        receivers_writer = csv.DictWriter(receivers_csvfile, fieldnames=receivers_fieldnames)
        receivers_writer.writeheader()

        for receiver in selected_receivers:
            receivers_writer.writerow(receiver)

        print(f"File CSV destinatari {percentage}% generato con successo.")

    # Apre un file CSV per scrivere le transazioni
    transactions_csv_filename = f'transazioni_{percentage}%.csv'
    with open(transactions_csv_filename, 'w', newline='') as transactions_csvfile:
        transactions_fieldnames = ['transaction_id', 'sender_id', 'receiver_id', 'transaction_type', 'Importo', 'transaction_date']
        transactions_writer = csv.DictWriter(transactions_csvfile, fieldnames=transactions_fieldnames)
        transactions_writer.writeheader()

        for transaction in selected_transactions:
            transactions_writer.writerow(transaction)

        print(f"File CSV transazioni {percentage}% generato con successo.")
