from fastapi import APIRouter, Request, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import auth_utils
from conf import KnownErrors
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
