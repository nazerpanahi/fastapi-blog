from sqlalchemy.orm import Session

from db.modelcrud import ModelCRUD
from models import Post
from schemas import PostCreate


class PostCRUD(ModelCRUD):
    def __init__(self, posts_db: Session):
        super().__init__(Post, posts_db)

    def get_by_id(self, post_id: int):
        return self.get_first(Post.post_id == post_id)

    def get_by_author(self, author_id: int):
        return self.filter(Post.author_id == author_id)

    def add_new_post(self, post: PostCreate):
        super().add_new(title=post.title, content=post.content, author_id=post.author_id)

    def delete_by_id(self, post_id: int):
        return self.delete(Post.post_id == post_id)

    def update_by_id(self, post_id: int, values: dict):
        return self.update(values, Post.post_id == post_id)
