from fastapi import APIRouter

from horreum.schema import node as api
from horreum.provider import node as provider


router = APIRouter()


@router.get("/templates/nodes",
            name="List node templates",
            description="Fetch list of all available node templates",
            response_model=api.NodeTemplateListResponse,
            tags=["node"])
async def list_nodes():
    node_templates = provider.list_nodes()
    response = {"items": node_templates}
    return response
