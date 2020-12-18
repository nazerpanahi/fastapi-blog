from sqlalchemy.orm import Session

from db.modelcrud import ModelCRUD
from models import UserPostLike


class UserPostLikeCRUD(ModelCRUD):
    def __init__(self, user_post_like_db: Session):
        super().__init__(UserPostLike, user_post_like_db)

    def user_post_like_exists(self, user_id: int, post_id: int):
        return super().exists(UserPostLike.user_id == user_id, UserPostLike.post_id == post_id)

    def like_post(self, user_id: int, post_id: int):
        return self.add_new(post_id=post_id, user_id=user_id)

    def get_liked_posts(self, user_id: int):
        return self.filter(UserPostLike.user_id == user_id)

    def get_users_like_post(self, post_id: int):
        return self.filter(UserPostLike.post_id == post_id)

    def unlike_post(self, user_id: int, post_id: int):
        return self.delete(UserPostLike.user_id == user_id, UserPostLike.post_id == post_id)
