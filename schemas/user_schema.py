from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserCreate(UserBase):
    password: str
    created_at: Optional[date]


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True
