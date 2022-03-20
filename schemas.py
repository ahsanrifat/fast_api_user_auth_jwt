from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    is_active: bool
    type: str


class UserView(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserViewList(BaseModel):
    status: bool
    user_list: List[UserView]

    class Config:
        orm_mode = True
