from fastapi import APIRouter, Request, Depends
from redis import Redis
from sqlalchemy.orm import Session

from conf.api import post_apis
from core.errors import KnownErrors
from core.responses import ok_response
from crud import PostCRUD
from schemas import PostCreate
from utils import auth_utils
from utils.db_utils import get_sql_db, get_redis_db

router = APIRouter()


@router.api_route(**post_apis.get('new'))
def new_post(request: Request,
             post: PostCreate,
             users_db: Session = Depends(get_sql_db),
             posts_db: Session = Depends(get_sql_db),
             tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    if post.author_id is None:
        post.author_id = user_id
    elif post.author_id != user_id:
        raise KnownErrors.ERROR_BAD_REQUEST
    PostCRUD(posts_db=posts_db).add_new_post(post=post)
    return ok_response()


@router.api_route(**post_apis.get('me_all'))
def get_all_my_posts(request: Request,
                     users_db: Session = Depends(get_sql_db),
                     posts_db: Session = Depends(get_sql_db),
                     tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    posts = PostCRUD(posts_db=posts_db).get_by_author(author_id=user_id)
    return ok_response(posts.all())


@router.api_route(**post_apis.get('all'))
def get_all_posts(request: Request,
                  posts_db: Session = Depends(get_sql_db),
                  tokens_db: Redis = Depends(get_redis_db)):
    # check if the user is authenticated and raise error if the token is not sent
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    # get all posts
    posts = PostCRUD(posts_db=posts_db).get_all()
    return ok_response(posts.all())


@router.api_route(**post_apis.get('get'))
def get_post(request: Request,
             post_id: int,
             posts_db: Session = Depends(get_sql_db),
             tokens_db: Redis = Depends(get_redis_db)):
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    post = PostCRUD(posts_db=posts_db).get_by_id(post_id=post_id)
    return ok_response(post)


@router.api_route(**post_apis.get('delete'))
def delete_post(request: Request,
                post_id: int,
                users_db: Session = Depends(get_sql_db),
                posts_db: Session = Depends(get_sql_db),
                tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    post_author_id = PostCRUD(posts_db=posts_db).get_by_id(post_id).author_id
    if post_author_id == user_id:  # check post owner
        post = PostCRUD(posts_db=posts_db).delete_by_id(post_id=post_id)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response(data=post)


@router.api_route(**post_apis.get('edit'))
def edit_post(request: Request,
              post_id: int,
              post: dict,
              users_db: Session = Depends(get_sql_db),
              posts_db: Session = Depends(get_sql_db),
              tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    post_author_id = PostCRUD(posts_db=posts_db).get_by_id(post_id).author_id
    if post_author_id == user_id:  # check post owner
        PostCRUD(posts_db=posts_db).update_by_id(post_id=post_id, values=post)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response()
