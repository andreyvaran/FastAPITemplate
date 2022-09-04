from .client import TagData

from pydantic import BaseModel
from typing import List
class TagFullData(BaseModel):
    id : int
    name: str
    description: str

    class Config:
        orm_mode = True


class CreateTag(TagData):
    pass

class CreateTagResponse(BaseModel):
    tag_id: int


class ReadTagResponse(BaseModel):
    tags: List[TagFullData]