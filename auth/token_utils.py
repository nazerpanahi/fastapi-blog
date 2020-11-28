from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from redis import Redis

from conf.constants import default_token_expire_minutes
from conf.settings import JWT_SETTINGS
from db.rediscrud import RedisCRUD
from schemas import User

_SEC_KEY = JWT_SETTINGS.get("SECRET_KEY", None)
_ALGO = JWT_SETTINGS.get("ALGORITHM", 'HS256')


def get_token_string(data: dict, expires_delta: Optional[timedelta] = None):
    """Tokenize data and set expire date for that"""
    to_encode = data.copy()
    expire = get_expire_date(expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _SEC_KEY, algorithm=_ALGO)
    return str(encoded_jwt)


def get_expire_date(expires_delta: Optional[timedelta] = None):
    """Calculate the expire date"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = get_default_expire_date()
    return expire


def get_default_expire_date():
    """Return now + default minutes"""
    return datetime.utcnow() + timedelta(minutes=default_token_expire_minutes)


def jwt_token_decode(token: str):
    """Decode jwt token"""
    return jwt.decode(token, _SEC_KEY, algorithms=[_ALGO])


def register_token_for_user(access_token: str, user: User, tokens_db: Redis):
    """set the access token and expire time for user"""
    expires_delta = timedelta(minutes=default_token_expire_minutes)
    return RedisCRUD(tokens_db).setex(user.username, expires_delta, access_token)


def token_exists(username: str, tokens_db: Redis):
    """check if the username has any token in the database or not"""
    return RedisCRUD(tokens_db).exists(username) != 0


def validate_token(username: str, token: str, tokens_db: Redis):
    """check if the user.token == token"""
    token_in_db = RedisCRUD(tokens_db).get(username)
    if token_in_db is None:
        return False
    return token_in_db.decode('utf-8') == token


def delete_user_token(username: str, tokens_db: Redis):
    """delete the user token in the database"""
    return RedisCRUD(tokens_db).delete(username)


def delete_token(token: str, tokens_db: Redis):
    data = jwt_token_decode(token)
    if 'username' in data:
        username = data.get('username')
        delete_user_token(username, tokens_db)
        return True
    else:
        return False
