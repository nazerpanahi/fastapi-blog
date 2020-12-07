from sqlalchemy.orm import Session

from db.modelcrud import ModelCRUD
from models import Comment
from schemas import CommentCreate


class CommentCRUD(ModelCRUD):
    def __init__(self, comments_db: Session):
        super().__init__(Comment, comments_db)

    def get_by_id(self, comment_id: int):
        return self.get_first(Comment.comment_id == comment_id)

    def get_by_author(self, author_id: int):
        return self.filter(Comment.author_id == author_id)

    def get_by_post(self, post_id: int):
        return self.filter(Comment.post_id == post_id)

    def add_new_comment(self, comment: CommentCreate):
        return super().add_new(post_id=comment.post_id, content=comment.content, author_id=comment.author_id)

    def delete_by_id(self, comment_id: int):
        return self.delete(Comment.comment_id == comment_id)

    def update_by_id(self, comment_id: int, values: dict):
        return self.update(values, Comment.comment_id == comment_id)
