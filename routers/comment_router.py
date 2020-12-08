from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from redis import Redis

from broker.tasks import save_data_in_elastic
from conf.api import comment_apis
from conf.settings import ELASTICSEARCH_SETTINGS
from core.errors import KnownErrors
from schemas import CommentCreate
from crud import CommentCRUD
from utils import auth_utils
from utils.db_utils import get_sql_db, get_redis_db
from core.responses import ok_response

router = APIRouter()


@router.api_route(**comment_apis.get('new'))
def new_comment(request: Request,
                comment: CommentCreate,
                users_db: Session = Depends(get_sql_db),
                comments_db: Session = Depends(get_sql_db),
                tokens_db: Redis = Depends(get_redis_db)):
    """Add new comment. Users can comment a post."""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    if comment.author_id is None:
        comment.author_id = user_id
    elif not check_comment_owner(comment.author_id, user_id):
        raise KnownErrors.ERROR_BAD_REQUEST
    comment_db = CommentCRUD(
        comments_db=comments_db
    ).add_new_comment(comment=comment)
    data = {
        'id': comment_db.comment_id,
        'content': comment_db.content,
        'created_at': comment_db.created_at,
        'author_id': comment_db.author_id,
        'post_id': comment_db.post_id,
    }
    save_data_in_elastic.apply_async(
        (data, ELASTICSEARCH_SETTINGS['indexes']['comment'])
    )
    return ok_response(comment_db)


@router.api_route(**comment_apis.get('me_all'))
def get_my_comments(request: Request,
                    users_db: Session = Depends(get_sql_db),
                    comments_db: Session = Depends(get_sql_db),
                    tokens_db: Redis = Depends(get_redis_db)):
    """Get all posts of current user"""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    comments = CommentCRUD(
        comments_db=comments_db
    ).get_by_author(author_id=user_id)
    return ok_response(comments.all())


@router.api_route(**comment_apis.get('all'))
def get_all_comments_of_specific_post(request: Request,
                                      post_id: int,
                                      comments_db: Session = Depends(get_sql_db),
                                      tokens_db: Redis = Depends(get_redis_db)):
    """Get all comment of a specific post"""
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    comments = CommentCRUD(
        comments_db=comments_db
    ).get_by_post(post_id=post_id)
    return ok_response(comments.all())


@router.api_route(**comment_apis.get('get'))
def get_comment(request: Request,
                comment_id: int,
                comments_db: Session = Depends(get_sql_db),
                tokens_db: Redis = Depends(get_redis_db)):
    """Get a specific comment"""
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    comment = CommentCRUD(
        comments_db=comments_db
    ).get_by_id(comment_id=comment_id)
    return ok_response(comment)


@router.api_route(**comment_apis.get('delete'))
def delete_comment(request: Request,
                   comment_id: int,
                   users_db: Session = Depends(get_sql_db),
                   comments_db: Session = Depends(get_sql_db),
                   tokens_db: Redis = Depends(get_redis_db)):
    """Delete a specific comment"""
    if validate_comment_owner(request, comment_id, users_db, tokens_db, comments_db):
        comment = CommentCRUD(
            comments_db=comments_db
        ).delete_by_id(comment_id=comment_id)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response(data=comment)


@router.api_route(**comment_apis.get('edit'))
def edit_comment(request: Request,
                 comment_id: int,
                 comment: dict,
                 users_db: Session = Depends(get_sql_db),
                 comments_db: Session = Depends(get_sql_db),
                 tokens_db: Redis = Depends(get_redis_db)):
    """Edit a specific comment"""
    if validate_comment_owner(request, comment_id, users_db, tokens_db, comments_db):
        CommentCRUD(
            comments_db=comments_db
        ).update_by_id(comment_id=comment_id, values=comment)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response()


def validate_comment_owner(request: Request, comment_id: int, users_db: Session, tokens_db: Redis, comments_db: Session):
    """Check if the current user is the author of the comment or not"""
    user_id = auth_utils.get_request_user(request, users_db, tokens_db).user_id
    comment_author_id = CommentCRUD(
        comments_db=comments_db
    ).get_by_id(comment_id).author_id
    return check_comment_owner(comment_author_id, user_id)


def check_comment_owner(comment_author_id, user_id):
    """compare user id and comment author id and return true if they are equal"""
    return user_id == comment_author_id
