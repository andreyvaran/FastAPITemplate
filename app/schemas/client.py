from typing import List, Optional

from pydantic import BaseModel


class TagData(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True



class Tag(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserData(BaseModel):
    telephone: str
    operator_code: str
    timestamp: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    user: UserData
    tags: List[TagData] = []

    class Config:
        orm_mode = True


class CreateUserResponse(BaseModel):
    user_id: int
