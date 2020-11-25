DB_SETTINGS = {
    'SQL': {
        'db_url': 'sqlite:///./database.db',
        'autocommit': False,
        'autoflush': False,
        'connect_args': {
            'check_same_thread': False
        }
    },
    'SEARCH_ENGINES': {
        'db_url': 'elasticsearch+http://localhost:9200/',
        'autocommit': False,
        'autoflush': False,
    },
}

JWT_SETTINGS = {
    'SECRET_KEY': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES': 30,
}
