from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import auth_utils, token_utils
from conf.constants import default_token_expire_minutes
from conf.errors import KnownErrors
from crud import crud_user
from db.utils import get_sql_db, get_redis_db
from schemas import UserCreate

router = APIRouter()


@router.post('/register', tags=['Authentication'], name='register')
def register(request: Request,
             user: UserCreate,
             users_db: Session = Depends(get_sql_db),
             tokens_db=Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request, tokens_db)  # Return None if the user is not authenticated
    if access_token is None:  # request is not authorized
        try:
            user_db = crud_user.UserCRUD(users_db=users_db).add_new_user(user)
            return user_db
        except IntegrityError:
            raise KnownErrors.ERROR_USER_EXISTS
    else:
        raise KnownErrors.ERROR_BAD_REQUEST


@router.post('/login', tags=['Authentication'], name='login')
def login(request: Request,
          user: UserCreate,
          users_db: Session = Depends(get_sql_db),
          tokens_db=Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request, tokens_db)  # Return None if the user is not authenticated
    if access_token is None:  # request is not authorized
        access_token = auth_utils.login_for_access_token(user.username,
                                                         user.password,
                                                         default_token_expire_minutes,
                                                         users_db,
                                                         tokens_db)
    resp = Response(headers={"Authorization": f"Bearer {access_token}"}, content=access_token)
    return resp


@router.post('/logout', tags=['Authentication'], name='logout')
def logout(request: Request,
           tokens_db=Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request, tokens_db)  # Return None if the user is not authenticated
    if access_token is None:  # request is not authorized
        return KnownErrors.ERROR_BAD_REQUEST
    b = token_utils.delete_token(token=access_token, tokens_db=tokens_db)
    if b:
        return {"message": "OK"}
    else:
        return {"message": "NOK"}
