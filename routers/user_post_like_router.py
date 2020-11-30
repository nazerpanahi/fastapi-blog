from fastapi import APIRouter, Request, Depends
from redis import Redis
from sqlalchemy.orm import Session

from conf.api import like_apis
from core.errors import KnownErrors
from core.responses import ok_response
from crud import PostCRUD, UserPostLikeCRUD
from utils import auth_utils
from utils.db_utils import get_sql_db, get_redis_db

router = APIRouter()


@router.get(like_apis.get('like'))
def like_post(request: Request,
              post_id: int,
              users_db: Session = Depends(get_sql_db),
              posts_db: Session = Depends(get_sql_db),
              user_post_like_db: Session = Depends(get_sql_db),
              tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    if PostCRUD(posts_db=posts_db).get_by_id(post_id=post_id) is None:
        raise KnownErrors.ERROR_BAD_REQUEST
    UserPostLikeCRUD(user_post_like_db=user_post_like_db).like_post(post_id=post_id, user_id=user_id)
    return ok_response()


@router.get(like_apis.get('unlike'))
def unlike_post(request: Request,
                post_id: int,
                users_db: Session = Depends(get_sql_db),
                posts_db: Session = Depends(get_sql_db),
                user_post_like_db: Session = Depends(get_sql_db),
                tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    if PostCRUD(posts_db=posts_db).get_by_id(post_id=post_id) is None:
        raise KnownErrors.ERROR_BAD_REQUEST
    UserPostLikeCRUD(user_post_like_db=user_post_like_db).unlike_post(post_id=post_id, user_id=user_id)
    return ok_response()


@router.get(like_apis.get('liked'))
def get_liked_posts(request: Request,
                    users_db: Session = Depends(get_sql_db),
                    user_post_like_db: Session = Depends(get_sql_db),
                    tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    token_user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    liked_posts = UserPostLikeCRUD(user_post_like_db=user_post_like_db).get_liked_posts(user_id=token_user_id)
    return ok_response(data=liked_posts)


@router.get(like_apis.get('likes'))
def get_post_likes(request: Request,
                   post_id: int,
                   posts_db: Session = Depends(get_sql_db),
                   user_post_like_db: Session = Depends(get_sql_db),
                   tokens_db: Redis = Depends(get_redis_db)):
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    if PostCRUD(posts_db=posts_db).get_by_id(post_id=post_id) is None:
        raise KnownErrors.ERROR_BAD_REQUEST
    likes = UserPostLikeCRUD(user_post_like_db=user_post_like_db).get_users_like_post(post_id=post_id).all()
    return ok_response(data=likes)
