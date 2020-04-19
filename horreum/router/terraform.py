from fastapi import APIRouter
from typing import List

from horreum.schema import terraform
from horreum.provider import terraform as provider


router = APIRouter()


@router.get("/resources",
            name="List Terraform resources",
            description="Fetch list of all supported Terraform resources",
            response_model=List[terraform.TerraformResource],
            tags=["Terraform"])
async def list_resources():
    objects = provider.list_resources()
    return objects
