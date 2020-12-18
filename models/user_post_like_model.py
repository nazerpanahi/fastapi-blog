from sqlalchemy import Column, ForeignKey, Integer

# from conf.constants import db_user_post_like_table_name, db_user_table_name, db_post_table_name
from utils.model_utils import get_table_name, get_table_column_name, get_column_address
from db.database import SQL_Base


class UserPostLike(SQL_Base):
    __tablename__ = get_table_name('user_post_like')

    post_id = Column(
        get_table_column_name('user_post_like', 'post_id'),
        Integer,
        ForeignKey(get_column_address('post', 'post_id')),
        primary_key=True
    )
    user_id = Column(
        get_table_column_name('user_post_like', 'user_id'),
        Integer,
        ForeignKey(get_column_address('user', 'user_id')),
        primary_key=True
    )
