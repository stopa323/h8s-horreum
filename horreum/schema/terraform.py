from pydantic import BaseModel, Field
from typing import List


class ResourceAttribute(BaseModel):
    name: str
    description: str
    read_only: bool = Field(True, alias="readOnly")

    class Config:
        orm_mode = True


class Resource(BaseModel):
    id: str
    name: str
    attributes: List[ResourceAttribute]

    class Config:
        orm_mode = True
