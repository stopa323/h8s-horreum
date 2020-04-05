from fastapi import APIRouter
from typing import List

from horreum.obj import terraform


router = APIRouter()


@router.get("/objects",
            name="Get Terraform objects",
            description="Fetch all supported Terraform objects.",
            response_model=List[terraform.GenericObject])
async def get_objects():
    items = []
    return items
