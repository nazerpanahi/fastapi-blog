from sqlalchemy.orm import Session

from db.modelcrud import ModelCRUD
from models import User
from schemas import UserCreate
from utils.password_utils import get_password_hash


class UserCRUD(ModelCRUD):
    def __init__(self, users_db: Session):
        super().__init__(User, users_db)

    def get_by_id(self, user_id: int) -> User:
        return self.get_first(User.user_id == user_id)

    def get_by_username(self, username: str) -> User:
        return self.get_first(User.username == username)

    def add_new_user(self, user: UserCreate):
        return super().add_new(username=user.username, first_name=user.first_name, last_name=user.last_name,
                               password=get_password_hash(user.password))

    def delete_by_id(self, user_id: int):
        return self.delete(User.user_id == user_id)

    def delete_by_username(self, username: str):
        return self.delete(User.username == username)

    def update_by_id(self, user_id: int, values: dict):
        return self.update(values, User.user_id == user_id)

    def update_by_username(self, username: str, values: dict):
        return self.update(values, User.username == username)

    def username_exists(self, username: str):
        return super().exists(User.username == username)
