from sqlalchemy import Column, ForeignKey, Integer

from conf.constants import db_user_post_like_table_name, db_user_table_name, db_post_table_name
from db.database import SQL_Base


class UserPostLike(SQL_Base):
    __tablename__ = db_user_post_like_table_name

    post_id = Column(
        Integer,
        ForeignKey(f"{db_post_table_name}.post_id"),
        primary_key=True
    )
    user_id = Column(Integer, ForeignKey(
        f"{db_user_table_name}.user_id"), primary_key=True)
