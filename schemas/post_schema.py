from datetime import date
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    author_id: Optional[int]


class PostCreate(PostBase):
    created_at: Optional[date]


class Post(PostBase):
    post_id: int

    class Config:
        orm_mode = True
