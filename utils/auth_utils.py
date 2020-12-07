from datetime import timedelta

from fastapi import Request
from jose import jwt, JWTError
from redis import Redis
from sqlalchemy.orm import Session

from conf.constants import token_header_key as TOKEN_HEADER_KEY
from core.errors import KnownErrors
from crud import UserCRUD
from schemas import UserCreate
from utils.token_utils import _SEC_KEY, _ALGO
from .password_utils import verify_password
from .token_utils import register_token_for_user, get_token_string, jwt_token_decode, validate_token


def authenticate_user(username: str, password: str, users_db: Session):
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


def get_current_user(access_token: str, users_db: Session):
    """Return current authenticated user"""
    credentials_exception = KnownErrors.ERROR_NOT_VALID_CREDENTIALS
    try:
        payload = jwt.decode(access_token, _SEC_KEY, algorithms=[_ALGO])
        username: str = payload.get("username")
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
                     token_header_key: str = TOKEN_HEADER_KEY,
                     error=None,
                     callback=None,
                     args=None,
                     kwargs=None):
    """check if the user is authenticated before or not using the request headers and
    return None or raise error or call callback function if the token is not sent (request is not authenticated) and
    raise not valid credentials error if credentials that sent in the request is not valid and
    return access token if none of the above conditions occur"""
    if is_token_sent(request, token_header_key):
        access_token = get_token_from_request(request, token_header_key)
        if not validate_request_token(access_token, tokens_db):
            raise KnownErrors.ERROR_NOT_VALID_CREDENTIALS
        return access_token
    else:
        if error is not None:
            raise error
        if callback is not None:
            if kwargs is None:
                kwargs = dict()
            if args is None:
                args = list()
            return callback(*args, **kwargs)
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


def get_request_user(request: Request, users_db: Session, tokens_db: Redis, error=KnownErrors.ERROR_BAD_REQUEST):
    """get the current user from the request headers and return the user"""
    access_token = is_authenticated(request=request,
                                    tokens_db=tokens_db,
                                    error=error)
    return get_current_user(access_token=access_token, users_db=users_db)
