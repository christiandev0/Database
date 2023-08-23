queries = {
    '1°': [
        # Trova transazioni con importo superiore a $10,000 e mittente/destinatario sospetto
        {
            '$and': [
                {'Importo': {'$gt': 10000}},
                {'$or': [
                    {'Mittente': 'MittenteSospetto'},
                    {'Destinatario': 'DestinatarioSospetto'}
                ]}
            ]
        },
        # Trova transazioni con data nell'ultimo semestre
        {
            'Data': {
                '$gte': '2023-01-01T00:00:00Z',
                '$lte': '2023-06-30T23:59:59Z'
            }
        },
        # Calcola la somma totale degli importi
        {'$group': {'_id': None, 'totalAmount': {'$sum': '$Importo'}}}
    ],
    '2°': [
        # Trova transazioni con importo superiore a $5,000 e mittente/destinatario sospetto
        {
            '$and': [
                {'Importo': {'$gt': 5000}},
                {'$or': [
                    {'Mittente': 'MittenteSospetto'},
                    {'Destinatario': 'DestinatarioSospetto'}
                ]}
            ]
        },
        # Trova transazioni con data nell'ultimo anno
        {
            'Data': {
                '$gte': '2022-08-01T00:00:00Z',
                '$lte': '2023-07-31T23:59:59Z'
            }
        },
        # Calcola la media degli importi
        {'$group': {'_id': None, 'averageAmount': {'$avg': '$Importo'}}}
    ],
    '3°': [
        # Trova transazioni con importo superiore a $1,000 e mittente/destinatario sospetto
        {
            '$and': [
                {'Importo': {'$gt': 1000}},
                {'$or': [
                    {'Mittente': 'MittenteSospetto'},
                    {'Destinatario': 'DestinatarioSospetto'}
                ]}
            ]
        },
        # Trova transazioni con data nell'ultimo anno
        {
            'Data': {
                '$gte': '2022-08-01T00:00:00Z',
                '$lte': '2023-07-31T23:59:59Z'
            }
        },
        # Trova transazioni con valuta diversa da USD o EUR
        {'Valuta': {'$nin': ['USD', 'EUR']}},
        # Calcola la somma totale degli importi per ciascun mese
        {
            '$group': {
                '_id': {'$month': '$Data'},
                'totalAmount': {'$sum': '$Importo'}
            }
        },
        # Ordina per mese crescente
        {'$sort': {'_id': 1}}
    ],
    '4°': [
        # Trova transazioni con importo superiore a $500 e mittente/destinatario sospetto
        {
            '$and': [
                {'Importo': {'$gt': 500}},
                {'$or': [
                    {'Mittente': 'MittenteSospetto'},
                    {'Destinatario': 'DestinatarioSospetto'}
                ]}
            ]
        },
        # Trova transazioni con data nell'ultimo anno
        {
            'Data': {
                '$gte': '2022-08-01T00:00:00Z',
                '$lte': '2023-07-31T23:59:59Z'
            }
        },
        # Trova transazioni con valuta diversa da USD o EUR
        {'Valuta': {'$nin': ['USD', 'EUR']}},
        # Calcola la somma totale degli importi per ciascun giorno della settimana
        {
            '$group': {
                '_id': {'$dayOfWeek': '$Data'},
                'totalAmount': {'$sum': '$Importo'}
            }
        },
        #Ordina per giorno della settimana crescente
        {'$sort': {'_id': 1}}
    ]
}
