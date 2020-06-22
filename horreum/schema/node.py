from pydantic import BaseModel, Field
from typing import List, Optional

# Todo: Improve Resources documentation


class PortTemplate(BaseModel):
    name: str = Field(...,
                      title="Port name")
    kind: str = Field(...,
                      title="Port kind")
    hasDefault: Optional[bool] = Field(False,
                                       title="Whether port has default value. "
                                             "Defaults to False")
    defaultValue: Optional[str] = Field(None,
                                        title="Default value")

    class Config:
        orm_mode = True

        schema_extra = {
            "description": "Port template object",
            "example": {
                "name": "CIDR",
                "description": "The CIDR block for the VPC",
                "defaultValue": "10.0.0.0/16"}}


class NodeTemplateCreate(BaseModel):
    name: str = Field(...,
                      title="Name displayed in GUI",
                      min_length=3, max_length=64)
    description: str = Field("",
                             title="Brief desciption of functionality provided"
                                   "by given node",
                             max_length=500)
    automoton: str = Field(...,
                           title="Name of the automoton responsible for node"
                                 "execution")
    # Todo: Handle kinds (module, resource) in metadata
    keywords: List[str] = Field([],
                                title="Collection of associated keywords, used"
                                      "for searching")
    ingressPorts: List[PortTemplate] = Field(
        [], title="Ordered collection of ingress ports")
    egressPorts: List[PortTemplate] = Field(
        [], title="Ordered collection of egress ports")

    class Config:
        orm_mode = True

        # Todo: Add example


class NodeTemplate(NodeTemplateCreate):
    id: str = Field(...,
                    title="Unique resource Id")

    class Config:
        orm_mode = True

        # Todo: Add example


class NodeTemplateListResponse(BaseModel):
    items: List[NodeTemplate] = Field(...,
                                      title="List of matched node templates")

    class Config:
        orm_mode = True
