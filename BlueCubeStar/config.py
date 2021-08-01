configs = {
    'cloudpiercer': {
        'IP': '0.0.0.0',
        'port': 8000,
        'table': 'MCV_table',
        'db': {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root'
        },
        'pandora_server': ('test', 'atomheart'),
        'atomheart': {
            'safety': {
                'salt': '1'
            }
        }
    },
    'cyberkernal': {
        'sem_number': 8,
        'default_expand': ['test'],
        'db':{
            'url': 'http://127.0.0.1:8000/'
        }
    }
    }
