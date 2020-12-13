from fastapi import status

default_token_expire_minutes = 15
token_header_key = 'Authorization'

error_user_exists = 'error_user_exists'
error_user_not_exists = 'error_user_not_exists'
error_not_authenticated = 'error_not_authenticated'
error_incorrect_username = 'error_incorrect_username'
error_incorrect_password = 'error_incorrect_password'
error_not_valid_credentials = 'error_not_valid_credentials'
error_user_not_found = 'error_user_not_found'
error_bad_request = 'error_bad_request'

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
