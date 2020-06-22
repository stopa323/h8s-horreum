from typing import List
from horreum.db.node import NodeTemplateObj
from horreum.schema import node as api

# Todo: Add method documentation


def list_nodes() -> List[NodeTemplateObj]:
    node_list = NodeTemplateObj.objects
    return list(node_list)


def load_node_fixture(node_template: api.NodeTemplateCreate) -> None:
    existing_node = NodeTemplateObj.objects(
        name=node_template.name, automoton=node_template.automoton)
    if existing_node:
        print(f"Node ({node_template.name}@{node_template.automoton}) already "
              f"exists. Skipping...")
        return

    node_obj = NodeTemplateObj(**node_template.dict())
    node_obj.save()
    print(f"Node ({node_template.name}@{node_template.automoton}) fixture "
          f"loaded.")
