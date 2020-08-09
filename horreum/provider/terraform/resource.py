from pynamodb.exceptions import DoesNotExist
from typing import List, Union

from horreum.api.schema import terraform as tf_api
from horreum.db import terraform as tf_db


def get_resource(resource_name: str) -> Union[tf_db.ResourceTemplateDB, None]:
    try:
        resource_tmpl_db = tf_db.ResourceTemplateDB.get(resource_name)
        return resource_tmpl_db
    except DoesNotExist:
        # LOG.info(f"Requested resource {resource_name} does not exist")
        return None


def list_resources() -> List[tf_db.ResourceTemplateDB]:
    resources = list(tf_db.ResourceTemplateDB.scan())
    return resources


def create_resource(resource_name: str,
                    resource: tf_api.PutTerraformResourceRequest) \
        -> tf_db.ResourceTemplateDB:
    new_resource = tf_db.ResourceTemplateDB(
        name=resource_name, **resource.dict())
    new_resource.save()
    return new_resource


def replace_resource(existing_resource: tf_db.ResourceTemplateDB,
                     new_resource: tf_api.PutTerraformResourceRequest) \
        -> tf_db.ResourceTemplateDB:
    existing_resource.description = new_resource.description
    existing_resource.attributes = [tf_db._ResourceAttribute(**attr.dict())
                                    for attr in new_resource.attributes]
    existing_resource.save()
    return existing_resource
