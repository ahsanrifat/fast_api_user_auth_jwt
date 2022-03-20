from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    is_active: bool
    type: str


class Item(BaseModel):
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class UserView(BaseModel):
    id: int
    name: str
    email: str
    items: List[Item]

    class Config:
        orm_mode = True


class UserViewList(BaseModel):
    status: bool
    user_list: List[UserView]

    class Config:
        orm_mode = True


class ItemView(BaseModel):
    title: str
    description: str
    owner: UserView

    class Config:
        orm_mode = True
