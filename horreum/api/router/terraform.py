# type: ignore
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from horreum.api.schema import terraform as tf_api
from horreum.provider import terraform as tf


router = APIRouter()


@router.get(path="/terraform/resources",
            name="List resources' templates.",
            description="Lists templates for supported Terraform resources.",
            response_model=tf_api.TerraformResourceCollection,
            tags=["terraform"])
async def list_resources():
    resources_db = tf.list_resources()
    resources_api = tf_api.TerraformResourceCollection(
        items=[r_db.to_dict() for r_db in resources_db])
    return resources_api


@router.put(path="/terraform/resources/{resource_name}",
            name="Put resource template at location.",
            description="Creates or updates Terraform resource template at "
                        "given location. If resource already exists, provided"
                        "data overwrites existing data.",
            response_model=tf_api.TerraformResource,
            responses={
                status.HTTP_200_OK: {
                    "description": "Existing resource template was replaced."},
                status.HTTP_201_CREATED: {
                    "description": "New resource template was created."}},
            tags=["terraform"])
async def put_resource(
        resource_name: str,
        resource: tf_api.PutTerraformResourceRequest):
    existing_resource = tf.get_resource(resource_name)

    if not existing_resource:
        new_resource = tf.create_resource(resource_name, resource)
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=tf_api.TerraformResource(
                **new_resource.to_dict()).dict(by_alias=True))
    else:
        updated_resource = tf.replace_resource(existing_resource, resource)
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content=tf_api.TerraformResource(
                **updated_resource.to_dict()).dict(by_alias=True))

    return response
