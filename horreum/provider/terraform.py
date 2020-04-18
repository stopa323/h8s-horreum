from typing import List
from horreum.db import terraform


def list_resources() -> List[terraform.Resource]:
    resources = terraform.Resource.objects
    return list(resources)
