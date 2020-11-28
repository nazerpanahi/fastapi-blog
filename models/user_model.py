from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from conf.constants import db_user_table_name
from db.database import SQL_Base, SE_Base


class User(SQL_Base, SE_Base):
    __tablename__ = db_user_table_name

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    password = Column(String)

    def __str__(self):
        return f"{self.user_id}-{self.username}"
