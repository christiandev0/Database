queries = {
    'Query 1': [
        {'Importo': {'$gt': 1000}},
        {
            '$and': [
                {'Mittente': 'MittenteSospetto'},
                {'Destinatario': 'DestinatarioSospetto'}
            ]
        },
        {
            '$or': [
                {'Importo': {'$gt': 500}},
                {
                    '$or': [
                        {'Mittente': 'MittenteSospetto'},
                        {'Destinatario': 'DestinatarioSospetto'}
                    ]
                }
            ]
        },
        {
            '$and': [
                {'Importo': {'$gt': 1000}},
                {'Mittente': 'MittenteSospetto'},
                {
                    'Data': {
                        '$gte': '2023-01-01T00:00:00Z',
                        '$lte': '2023-12-31T23:59:59Z'
                    }
                }
            ]
        }
    ],
    'Query 2': [{'Importo': {'$gt': 1000}},
           {
               '$and': [
                   {'Mittente': 'MittenteSospetto'},
                   {'Destinatario': 'DestinatarioSospetto'}
               ]
           },
           {
               '$or': [
                   {'Importo': {'$gt': 500}},
                   {
                       '$or': [
                           {'Mittente': 'MittenteSospetto'},
                           {'Destinatario': 'DestinatarioSospetto'}
                       ]
                   }
               ]
           },
           {
               '$and': [
                   {'Importo': {'$gt': 1000}},
                   {'Mittente': 'MittenteSospetto'},
                   {
                       'Data': {
                           '$gte': '2023-01-01T00:00:00Z',
                           '$lte': '2023-12-31T23:59:59Z'
                       }
                   }
               ]
           }],
    'Query 3': [{'Importo': {'$gt': 1000}},
           {
               '$and': [
                   {'Mittente': 'MittenteSospetto'},
                   {'Destinatario': 'DestinatarioSospetto'}
               ]
           },
           {
               '$or': [
                   {'Importo': {'$gt': 500}},
                   {
                       '$or': [
                           {'Mittente': 'MittenteSospetto'},
                           {'Destinatario': 'DestinatarioSospetto'}
                       ]
                   }
               ]
           },
           {
               '$and': [
                   {'Importo': {'$gt': 1000}},
                   {'Mittente': 'MittenteSospetto'},
                   {
                       'Data': {
                           '$gte': '2023-01-01T00:00:00Z',
                           '$lte': '2023-12-31T23:59:59Z'
                       }
                   }
               ]
           }],
    'Query 4': [{'Importo': {'$gt': 1000}},
            {
                '$and': [
                    {'Mittente': 'MittenteSospetto'},
                    {'Destinatario': 'DestinatarioSospetto'}
                ]
            },
            {
                '$or': [
                    {'Importo': {'$gt': 500}},
                    {
                        '$or': [
                            {'Mittente': 'MittenteSospetto'},
                            {'Destinatario': 'DestinatarioSospetto'}
                        ]
                    }
                ]
            },
            {
                '$and': [
                    {'Importo': {'$gt': 1000}},
                    {'Mittente': 'MittenteSospetto'},
                    {
                        'Data': {
                            '$gte': '2023-01-01T00:00:00Z',
                            '$lte': '2023-12-31T23:59:59Z'
                        }
                    }
                ]
            }]
}