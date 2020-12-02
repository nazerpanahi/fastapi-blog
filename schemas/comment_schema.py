from datetime import date
from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    created_at: Optional[date]
    author_id: Optional[int]
    post_id: int


class Comment(CommentBase):
    comment_id: int

    class Config:
        orm_mode = True
