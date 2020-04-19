from pydantic import BaseModel, Field
from typing import List


class TerraformResourceAttribute(BaseModel):
    name: str = Field(...,
                      title="Name of the attribute in Terraform configuration")
    description: str = Field("", title="Brief attribute description")
    read_only: bool = Field(True, alias="readOnly",
                            title="Flag describing if attribute is configurable"
                                  " or accessed only as resource output")

    class Config:
        orm_mode = True

        schema_extra = {
            "description": "Terraform resource attribute definition",
            "example": {
                "name": "cidr_block",
                "description": "The CIDR block for the VPC",
                "readOnly": False}}


class TerraformResource(BaseModel):
    id: str = Field(..., title="Unique ID ot the resource")
    name: str = Field(..., title="Resource name")
    attributes: List[TerraformResourceAttribute] = Field(
        ..., title="List of resource attributes")

    class Config:
        orm_mode = True

        schema_extra = {
            "description": "Terraform resource definition",
            "example": {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "aws_vpc",
                "attributes": [
                    TerraformResourceAttribute.Config.schema_extra["example"]]}}
