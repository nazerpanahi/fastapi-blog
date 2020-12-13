FAST_API_PORT = 8000

DB_SETTINGS = {
    'SQL': {
        'db_url': 'sqlite:///./database.sqlite',
        'autocommit': False,
        'autoflush': False,
        'connect_args': {
            'check_same_thread': False
        }
    },
}

REDIS_SETTINGS = {
    'host': 'localhost',
    'port': 6379
}

ELASTICSEARCH_SETTINGS = {
    'indexes': {
        'auth': 'test_auth',
        'post': 'test_post',
        'like': 'test_like',
        'comment': 'test_comment',
    }
}

JWT_SETTINGS = {
    'SECRET_KEY': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES': 30,
}

model_table_prefix = ''
model_tables = {
    'user': {
        'name': f'{model_table_prefix}users',
        'columns': {
            'user_id': 'user_id',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'created_at': 'created_at',
            'password': 'password',
        },
    },
    'post': {
        'name': f'{model_table_prefix}posts',
        'columns': {
            'post_id': 'post_id',
            'title': 'title',
            'content': 'content',
            'created_at': 'created_at',
            'author_id': 'author_id',
        },
    },
    'comment': {
        'name': f'{model_table_prefix}comments',
        'columns': {
            'comment_id': 'comment_id',
            'content': 'content',
            'created_at': 'created_at',
            'author_id': 'author_id',
            'post_id': 'post_id',
        },
    },
    'user_post_like': {
        'name': f'{model_table_prefix}user_post_like',
        'columns': {
            'post_id': 'post_id',
            'user_id': 'user_id',
        },
    },
}
