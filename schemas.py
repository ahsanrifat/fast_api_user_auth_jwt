from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    is_admin: Optional[bool] = False
    is_super_admin: Optional[bool] = False
