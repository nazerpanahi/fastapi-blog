from fastapi import APIRouter, Request, Depends, Response
from redis import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from conf.api import auth_apis
from conf.constants import default_token_expire_minutes
from core.errors import KnownErrors
from core.responses import ok_response, nok_response
from crud import crud_user
from schemas import UserCreate
from utils import auth_utils, token_utils
from utils.db_utils import get_sql_db, get_redis_db

router = APIRouter()


@router.api_route(**auth_apis.get('register'))
def register(request: Request,
             user: UserCreate,
             users_db: Session = Depends(get_sql_db),
             tokens_db: Redis = Depends(get_redis_db)):
    """Register the user in the database if the user has not registered before and has not logged in. Return the user
    after it created successfully"""
    access_token = auth_utils.is_authenticated(request, tokens_db,)
    if access_token is None:  # request is not authorized
        if crud_user.UserCRUD(users_db=users_db).username_exists(user.username):
            raise KnownErrors.ERROR_USER_EXISTS
        user_db = crud_user.UserCRUD(users_db=users_db).add_new_user(user)
        return ok_response(user_db)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST


@router.api_route(**auth_apis.get('login'))
def login(request: Request,
          user: UserCreate,
          users_db: Session = Depends(get_sql_db),
          tokens_db: Redis = Depends(get_redis_db)):
    """Login the user and return the token"""
    access_token = auth_utils.is_authenticated(request, tokens_db,
                                               callback=auth_utils.login_for_access_token,
                                               args=[user.username,
                                                     user.password,
                                                     default_token_expire_minutes,
                                                     users_db,
                                                     tokens_db],)
    resp = Response(headers={"Authorization": f"Bearer {access_token}"}, content=access_token)
    return resp


@router.api_route(**auth_apis.get('logout'))
def logout(request: Request,
           tokens_db: Redis = Depends(get_redis_db)):
    """Logout the user and delete the token"""
    access_token = auth_utils.is_authenticated(request, tokens_db, error=KnownErrors.ERROR_BAD_REQUEST)
    is_deleted = token_utils.delete_token(token=access_token, tokens_db=tokens_db)
    if is_deleted:
        return ok_response()
    else:
        return nok_response()


@router.api_route(**auth_apis.get('delete_account'))
def delete_account(request: Request,
                   users_db: Session = Depends(get_sql_db),
                   tokens_db: Redis = Depends(get_redis_db)):
    """Delete the user from database"""
    access_token = auth_utils.is_authenticated(request, tokens_db, error=KnownErrors.ERROR_BAD_REQUEST)
    user = auth_utils.get_current_user(access_token=access_token, users_db=users_db)
    resp = crud_user.UserCRUD(users_db=users_db).delete_by_username(username=user.username)
    return ok_response(data=resp)
