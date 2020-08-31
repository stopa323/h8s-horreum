from pydantic import BaseModel, Field
from typing import List, Optional


class ResourceAttribute(BaseModel):
    name: str = Field(
        ...,
        title="Attribute name.",
        min_length=2,
        max_length=64)
    description: Optional[str] = Field(
        None,
        title="Brief description of the attribute.",
        min_length=0,
        max_length=200)
    type: str = Field(
        ...,
        title="Attribute type.",
        min_length=3,
        max_length=32)
    is_argument: bool = Field(
        False,
        title="When set to true, indicates that this attribute is used as input"
              " for resource configuration. Note that every attribute can be "
              "referenced as output.",
        alias="isArgument")
    is_required: bool = Field(
        False, title="When set to true, indicates that input value for this "
                     "attribute must be provided.",
        alias="isRequired")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "description": "Terraform attribute",
            "example": {
                "name": "CIDR",
                "description": "The CIDR block for the VPC",
                "type": "String",
                "isArgument": True,
                "isRequired": True
            }
        }


class TerraformResource(BaseModel):
    name: str = Field(..., title="Resource name.", min_length=3, max_length=64)
    description: Optional[str] = Field(
        None, title="Brief description of the resource.", min_length=0,
        max_length=200)
    attributes: List[ResourceAttribute] = Field(
        [], title="Collection of resource attributes.")

    class Config:
        allow_population_by_field_name = True


class PutTerraformResourceRequest(BaseModel):
    # Todo: Override fields' description.
    description: Optional[str] = Field(
        None, title="Brief description of the resource.", min_length=0,
        max_length=200)
    attributes: List[ResourceAttribute] = Field(
        [], title="Collection of resource attributes.")

    class Config:
        allow_population_by_field_name = True


class TerraformResourceCollection(BaseModel):
    items: List[TerraformResource] = Field(
        [], title="Collection of Terraform resources.",
        alias="terraformResources")

    class Config:
        allow_population_by_field_name = True
