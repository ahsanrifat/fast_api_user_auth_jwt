from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    # id: int
    name: str
    email: str
    password: str
    is_active: bool
    type: str
