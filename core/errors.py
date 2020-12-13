from fastapi import HTTPException

from conf import constants


class KnownErrors:
    ERROR_USER_EXISTS = HTTPException(**constants.errors_settings[constants.error_user_exists])
    ERROR_USER_NOT_EXISTS = HTTPException(**constants.errors_settings[constants.error_user_not_exists])
    ERROR_NOT_AUTHENTICATED = HTTPException(**constants.errors_settings[constants.error_not_authenticated])
    ERROR_INCORRECT_USERNAME = HTTPException(**constants.errors_settings[constants.error_incorrect_username])
    ERROR_INCORRECT_PASSWORD = HTTPException(**constants.errors_settings[constants.error_incorrect_password])
    ERROR_NOT_VALID_CREDENTIALS = HTTPException(**constants.errors_settings[constants.error_not_valid_credentials])
    ERROR_USER_NOT_FOUND = HTTPException(**constants.errors_settings[constants.error_user_not_found])
    ERROR_BAD_REQUEST = HTTPException(**constants.errors_settings[constants.error_bad_request])
