import json

from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import (
    BooleanAttribute, ListAttribute, MapAttribute, UnicodeAttribute)
from os import getenv
from typing import Any, Optional

from horreum.common.config import get_config


class SerializableModel(Model):

    def to_json(self, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self) -> dict:
        ret_dict = {}
        for name, attr in self.attribute_values.items():
            ret_dict[name] = self._attr_to_obj(attr)

        return ret_dict

    def _attr_to_obj(self, attr: Any) -> Any:
        # compare with list class. It is not ListAttribute.
        if isinstance(attr, list):
            _list = []
            for l in attr:
                _list.append(self._attr_to_obj(l))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr_to_obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr


class _ResourceAttribute(MapAttribute):
    name = UnicodeAttribute(null=False)
    description = UnicodeAttribute(null=True)
    type = UnicodeAttribute(null=False)
    is_argument = BooleanAttribute(null=False)
    is_required = BooleanAttribute(null=False)


class ResourceTemplateDB(SerializableModel):
    class Meta:
        table_name = "terraform-resource-templates"

    name = UnicodeAttribute(hash_key=True)
    description = UnicodeAttribute(null=True)
    attributes = ListAttribute(of=_ResourceAttribute, default=[])
    # keywords = ListAttribute(of=str, default=[])
