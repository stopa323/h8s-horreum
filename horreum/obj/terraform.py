from pydantic import BaseModel, Field
from typing import List


class Attribute(BaseModel):
    name: str
    description: str
    read_only: bool = Field(True, alias="readOnly")


class GenericObject(BaseModel):
    name: str
    attributes: List[Attribute]
