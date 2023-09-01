import csv

nomsospetti = []
with open('nomsospetti.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        nomsospetti.append(row[0])

queries = {
    'Query 1': [
        # Query per transazioni con importo maggiore di 1000
        {'Importo': {'$lt': 1000}},
        # Transazioni da paesi extra-UE (Paese_a_Rischio è 'Sì')
        {'Paese_a_Rischio': 'Sì'},
        # Transazioni con metodo di pagamento diverso da 'Carta di credito'
        {'Metodo_di_pagamento': {'$ne': 'Carta di credito'}}
    ],
    'Query 2': [
        # Query per transazioni con importo maggiore di 2000
        {'Importo': {'$gt': 2000}},
        # Transazioni da paesi extra-UE (Paese_a_Rischio è 'Sì')
        {'Paese_a_Rischio': 'Sì'},
        # Transazioni con metodo di pagamento 'Bonifico'
        {'Metodo_di_pagamento': 'Bonifico'},
        # Transazioni con data antecedente al 30 giugno 2023
        {'Data': {'$lt': '2023-06-30T00:00:00Z'}}
    ],
    'Query 3': [
        # Transazioni con importo maggiore di 1500 da paesi extra-UE
        # oppure transazioni con metodo diverso da 'PayPal' da paesi UE
        {'$or': [
            {'$and': [
                {'Paese_a_Rischio': 'Sì'},
                {'Importo': {'$gt': 1500}}
            ]},
            {'$and': [
                {'Paese_a_Rischio': 'No'},
                {'Metodo_di_pagamento': {'$ne': 'PayPal'}}
            ]}
        ]},
        # Transazioni con data compresa tra l'1 gennaio e il 31 dicembre 2023
        {'Data': {'$gte': '2023-01-01T00:00:00Z', '$lte': '2023-12-31T23:59:59Z'}}
    ],
    'Query 4': [
        # Transazioni da paesi extra-UE con importo maggiore di 1500
        # e metodo di pagamento 'Assegno' oppure transazioni con mittente
        # o destinatario in nomsospetti con importo maggiore di 500
        {'$or': [
            {'$and': [
                {'Paese_a_Rischio': 'Sì'},
                {'$or': [
                    {'Mittente': {'$in': nomsospetti}},
                    {'Destinatario': {'$in': nomsospetti}}
                ]}
            ]},
            {'$and': [
                {'Importo': {'$gt': 1500}},
                {'Metodo_di_pagamento': 'Assegno'}
            ]}
        ]},
        # Transazioni con data successiva al 15 settembre 2023
        {'Data': {'$gt': '2023-09-15T00:00:00Z'}}
    ]
}
