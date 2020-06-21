from typing import List
from horreum.db.node import NodeTemplateObj


def list_nodes() -> List[NodeTemplateObj]:
    node_list = NodeTemplateObj.objects
    return list(node_list)
