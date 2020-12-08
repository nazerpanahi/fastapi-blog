from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Date, Text

from conf.constants import db_user_table_name, db_post_table_name, db_comment_table_name
from db.database import SQL_Base


class Comment(SQL_Base):
    __tablename__ = db_comment_table_name

    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(Date, default=datetime.now().date())
    author_id = Column(Integer, ForeignKey(f"{db_user_table_name}.user_id"))
    post_id = Column(Integer, ForeignKey(f"{db_post_table_name}.post_id"))
