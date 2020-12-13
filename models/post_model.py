from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text

from utils.model_utils import get_table_name, get_table_column_name, get_column_address
from db.database import SQL_Base


class Post(SQL_Base):
    __tablename__ = get_table_name('post')

    post_id = Column(
        get_table_column_name('post', 'post_id'),
        Integer,
        primary_key=True,
        index=True
    )
    title = Column(
        get_table_column_name('post', 'title'),
        Text,
        index=True
    )
    content = Column(
        get_table_column_name('post', 'content'),
        Text
    )
    created_at = Column(
        get_table_column_name('post', 'created_at'),
        DateTime, default=datetime.now()
    )
    # author_id = Column(Integer, ForeignKey(f"{db_user_table_name}.user_id"))
    author_id = Column(
        get_table_column_name('post', 'author_id'),
        Integer,
        ForeignKey(get_column_address('user', 'user_id'))
    )
