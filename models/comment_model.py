from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Date, Text

from utils.model_utils import get_table_name, get_table_column_name, get_column_address
from db.database import SQL_Base


class Comment(SQL_Base):
    __tablename__ = get_table_name('comment')

    comment_id = Column(
        get_table_column_name('comment', 'comment_id'),
        Integer,
        primary_key=True,
        index=True
    )
    content = Column(
        get_table_column_name('comment', 'content'),
        Text,
        nullable=False
    )
    created_at = Column(
        get_table_column_name('comment', 'created_at'),
        Date,
        default=datetime.now().date()
    )
    author_id = Column(
        get_table_column_name('comment', 'author_id'),
        Integer,
        ForeignKey(get_column_address('user', 'user_id'))
    )
    post_id = Column(
        get_table_column_name('comment', 'post_id'),
        Integer,
        ForeignKey(get_column_address('post', 'post_id'))
    )
