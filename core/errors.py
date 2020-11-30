from fastapi import HTTPException

from conf import constants


class KnownErrors:
    ERROR_USER_EXISTS = HTTPException(status_code=constants.error_user_exists_code,
                                      detail=constants.error_user_exists)
    ERROR_USER_NOT_EXISTS = HTTPException(status_code=constants.error_user_not_exists_code,
                                          detail=constants.error_user_not_exists)
    ERROR_NOT_AUTHENTICATED = HTTPException(status_code=constants.error_not_authenticated_code,
                                            detail=constants.error_not_authenticated)
    ERROR_INCORRECT_USERNAME = HTTPException(status_code=constants.error_incorrect_username_code,
                                             detail=constants.error_incorrect_username)
    ERROR_INCORRECT_PASSWORD = HTTPException(status_code=constants.error_incorrect_password_code,
                                             detail=constants.error_incorrect_password)
    ERROR_NOT_VALID_CREDENTIALS = HTTPException(status_code=constants.error_not_valid_credentials_code,
                                                detail=constants.error_not_valid_credentials)
    ERROR_USER_NOT_FOUND = HTTPException(status_code=constants.error_user_not_found_code,
                                         detail=constants.error_user_not_found)
    ERROR_BAD_REQUEST = HTTPException(status_code=constants.error_bad_request_code,
                                      detail=constants.error_bad_request)
