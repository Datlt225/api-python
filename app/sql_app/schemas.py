from pydantic import BaseModel
from typing import Optional


class UsersBase(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class CreateAccountRequest(UsersBase):
    pass
