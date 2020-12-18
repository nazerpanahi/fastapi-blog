from starlette import status

from conf.constants import error_user_exists, error_user_not_exists, error_not_authenticated, error_incorrect_username, \
    error_incorrect_password, error_not_valid_credentials, error_user_not_found, error_bad_request

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

errors_settings = {
    error_user_exists: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'User exists',
    },
    error_user_not_exists: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'User not exists',
    },
    error_not_authenticated: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Not Authenticated',
    },
    error_incorrect_username: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Incorrect username or password',
    },
    error_incorrect_password: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Incorrect username or password',
    },
    error_not_valid_credentials: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Could not validate credentials',
    },
    error_user_not_found: {
        'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'detail': 'User not found',
    },
    error_bad_request: {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'detail': 'Bad Request',
    },
}
