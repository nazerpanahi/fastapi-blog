from fastapi import HTTPException

import conf.settings
from conf import constants


class KnownErrors:
    ERROR_USER_EXISTS = HTTPException(**conf.settings.errors_settings[constants.error_user_exists])
    ERROR_USER_NOT_EXISTS = HTTPException(**conf.settings.errors_settings[constants.error_user_not_exists])
    ERROR_NOT_AUTHENTICATED = HTTPException(**conf.settings.errors_settings[constants.error_not_authenticated])
    ERROR_INCORRECT_USERNAME = HTTPException(**conf.settings.errors_settings[constants.error_incorrect_username])
    ERROR_INCORRECT_PASSWORD = HTTPException(**conf.settings.errors_settings[constants.error_incorrect_password])
    ERROR_NOT_VALID_CREDENTIALS = HTTPException(**conf.settings.errors_settings[constants.error_not_valid_credentials])
    ERROR_USER_NOT_FOUND = HTTPException(**conf.settings.errors_settings[constants.error_user_not_found])
    ERROR_BAD_REQUEST = HTTPException(**conf.settings.errors_settings[constants.error_bad_request])
