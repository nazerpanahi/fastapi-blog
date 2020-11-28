from datetime import timedelta

from fastapi import Depends, Request
from jose import jwt, JWTError
from redis import Redis
from sqlalchemy.orm import Session

from auth.token_utils import _SEC_KEY, _ALGO
from conf import KnownErrors, token_header_key as TOKEN_HEADER_KEY
from crud import UserCRUD
from db import utils
from schemas import UserCreate
from security import verify_password
from .token_utils import register_token_for_user, get_token_string, jwt_token_decode, validate_token


def authenticate_user(username: str, password: str, users_db: Session = Depends(utils.get_sql_db)):
    """Get the user credentials and check if the users credentials exist in database"""
    user_db = UserCRUD(users_db=users_db).get_by_username(username=username)
    if not user_db:
        raise KnownErrors.ERROR_INCORRECT_USERNAME
    user_dict = {
        "username": user_db.username,
        "password": user_db.password,
        "first_name": user_db.first_name,
        "last_name": user_db.last_name,
    }
    user = UserCreate(**user_dict)
    if not verify_password(password, user.password):
        raise KnownErrors.ERROR_INCORRECT_PASSWORD
    return user_db


def get_current_user(access_token: str, users_db: Session = Depends(utils.get_sql_db)):
    """Return current authenticated user"""
    credentials_exception = KnownErrors.ERROR_NOT_VALID_CREDENTIALS
    try:
        payload = jwt.decode(access_token, _SEC_KEY, algorithms=[_ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UserCRUD(users_db=users_db).get_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


def is_token_sent(request: Request, token_header_key: str = TOKEN_HEADER_KEY):
    """check if the request contains the token"""
    if token_header_key in request.headers:
        return True
    return False


def get_token_from_request(request: Request, token_header_key: str = TOKEN_HEADER_KEY):
    """extract token from request headers"""
    if is_token_sent(request):
        return request.headers[token_header_key].split(' ')[1]
    else:
        return None


def validate_request_token(token: str, tokens_db: Redis) -> bool:
    """check if the token is valid in the database or not"""
    if token is not None:
        data = jwt_token_decode(token)
        username = data.get('username', None)
        if validate_token(username, token, tokens_db):
            return True
    return False


def is_authenticated(request: Request,
                     tokens_db: Redis,
                     token_header_key: str = TOKEN_HEADER_KEY):
    """check if the user is authenticated before or not using the request headers"""
    if is_token_sent(request, token_header_key):
        access_token = get_token_from_request(request, token_header_key)
        if not validate_request_token(access_token, tokens_db):
            raise KnownErrors.ERROR_NOT_VALID_CREDENTIALS
        return access_token
    else:
        return None


def login_for_access_token(username, password, expire_delta, users_db: Session, tokens_db: Redis):
    """authenticate a user in the database and generate a new access token for user. return user access token"""
    user = authenticate_user(username, password, users_db)
    data = {
        "username": user.username,
        "password": user.password
    }
    expire_delta = timedelta(expire_delta)
    access_token = get_token_string(data, expire_delta)
    register_token_for_user(access_token, user, tokens_db)
    return access_token
