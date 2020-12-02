from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from redis import Redis
from conf.api import comment_apis
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
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db)
    if comment.author_id is None:
        comment.author_id = user_id
    elif comment.author_id != user_id:
        raise KnownErrors.ERROR_BAD_REQUEST
    CommentCRUD(comments_db=comments_db).add_new_comment(comment=comment)
    return ok_response()


@router.api_route(**comment_apis.get('me_all'))
def get_my_comments(request: Request,
                    users_db: Session = Depends(get_sql_db),
                    comments_db: Session = Depends(get_sql_db),
                    tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    comments = CommentCRUD(comments_db=comments_db).get_by_author(author_id=user_id)
    return ok_response(comments.all())


@router.api_route(**comment_apis.get('all'))
def get_all_comments_of_specific_post(request: Request,
                                      post_id: int,
                                      comments_db: Session = Depends(get_sql_db),
                                      tokens_db: Redis = Depends(get_redis_db)):
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    comments = CommentCRUD(comments_db=comments_db).get_by_post(post_id=post_id)
    return ok_response(comments.all())


@router.api_route(**comment_apis.get('get'))
def get_comment(request: Request,
                comment_id: int,
                comments_db: Session = Depends(get_sql_db),
                tokens_db: Redis = Depends(get_redis_db)):
    auth_utils.is_authenticated(request=request,
                                tokens_db=tokens_db,
                                error=KnownErrors.ERROR_BAD_REQUEST)
    comment = CommentCRUD(comments_db=comments_db).get_by_id(comment_id=comment_id)
    return ok_response(comment)


@router.api_route(**comment_apis.get('delete'))
def delete_comment(request: Request,
                   comment_id: int,
                   users_db: Session = Depends(get_sql_db),
                   comments_db: Session = Depends(get_sql_db),
                   tokens_db: Redis = Depends(get_redis_db)):
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    comment_author_id = CommentCRUD(comments_db=comments_db).get_by_id(comment_id).author_id
    if comment_author_id == user_id:
        comment = CommentCRUD(comments_db=comments_db).delete_by_id(comment_id=comment_id)
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
    access_token = auth_utils.is_authenticated(request=request,
                                               tokens_db=tokens_db,
                                               error=KnownErrors.ERROR_BAD_REQUEST)
    user_id = auth_utils.get_current_user(access_token=access_token, users_db=users_db).user_id
    post_author_id = CommentCRUD(comments_db=comments_db).get_by_id(comment_id).author_id
    if post_author_id == user_id:
        CommentCRUD(comments_db=comments_db).update_by_id(comment_id=comment_id, values=comment)
    else:
        raise KnownErrors.ERROR_BAD_REQUEST
    return ok_response()
