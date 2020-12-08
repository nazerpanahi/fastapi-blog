from fastapi import APIRouter, Request, Depends
from redis import Redis
from sqlalchemy.orm import Session

from broker.tasks import save_data_in_elastic
from conf.api import post_apis
from conf.settings import ELASTICSEARCH_SETTINGS
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
    """Add new post"""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    if post.author_id is None:
        post.author_id = user_id
    elif not check_post_owner(post.author_id, user_id):
        raise KnownErrors.ERROR_BAD_REQUEST
    post_db = PostCRUD(posts_db=posts_db).add_new_post(post=post)
    data = {
        'id': post_db.post_id,
        'title': post_db.title,
        'content': post_db.content,
        'created_at': post_db.created_at,
        'author_id': post_db.author_id,
    }
    save_data_in_elastic.apply_async(
        (data, ELASTICSEARCH_SETTINGS['indexes']['comment'])
    )
    return ok_response(post_db)


@router.api_route(**post_apis.get('me_all'))
def get_all_my_posts(request: Request,
                     users_db: Session = Depends(get_sql_db),
                     posts_db: Session = Depends(get_sql_db),
                     tokens_db: Redis = Depends(get_redis_db)):
    """Get all posts of current user"""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    posts = PostCRUD(posts_db=posts_db).get_by_author(author_id=user_id)
    return ok_response(posts.all())


@router.api_route(**post_apis.get('all'))
def get_all_posts(request: Request,
                  posts_db: Session = Depends(get_sql_db),
                  tokens_db: Redis = Depends(get_redis_db)):
    """Get all posts of all users"""
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
    """Get a specific post"""
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
    """Delete a specific post"""
    if validate_post_owner(request, post_id, users_db, tokens_db, posts_db):
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
    """Edit a specific post"""
    if validate_post_owner(request, post_id, users_db, tokens_db, posts_db):
        PostCRUD(posts_db=posts_db).update_by_id(post_id=post_id, values=post)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response()


def validate_post_owner(request: Request, post_id: int, users_db: Session, tokens_db: Redis, posts_db: Session):
    """Check if the current user is the author of the post or not"""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    post_author_id = PostCRUD(posts_db=posts_db).get_by_id(post_id).author_id
    return check_post_owner(post_author_id, user_id)


def check_post_owner(post_author_id, user_id):
    """compare user id and post author id and return true if they are equal"""
    return user_id == post_author_id
