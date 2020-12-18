from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

# from conf.constants import db_user_table_name
from utils.model_utils import get_table_name, get_table_column_name
from db.database import SQL_Base


class User(SQL_Base):
    __tablename__ = get_table_name('user')

    user_id = Column(
        get_table_column_name('user', 'user_id'),
        Integer,
        primary_key=True,
        index=True
    )
    username = Column(
        get_table_column_name('user', 'username'),
        String,
        unique=True,
        index=True
    )
    first_name = Column(
        get_table_column_name('user', 'first_name'),
        String,
        nullable=True
    )
    last_name = Column(
        get_table_column_name('user', 'last_name'),
        String,
        nullable=True
    )
    created_at = Column(
        get_table_column_name('user', 'created_at'),
        DateTime,
        default=datetime.now(),
        nullable=False
    )
    password = Column(
        get_table_column_name('user', 'password'),
        String
    )

    def __str__(self):
        return f"{self.user_id}-{self.username}"
