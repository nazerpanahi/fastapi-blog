from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text

from conf.constants import db_user_table_name, db_post_table_name
from db.database import SQL_Base


class Post(SQL_Base):
    __tablename__ = db_post_table_name

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey(f"{db_user_table_name}.user_id"))
