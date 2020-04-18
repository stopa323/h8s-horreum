import mongoengine as me

from horreum.db import base


class ResourceAttribute(me.EmbeddedDocument):
    name = me.StringField()
    description = me.StringField()
    read_only = me.BooleanField()


class Resource(base.HasId):
    name = me.StringField()
    attributes = me.ListField(me.EmbeddedDocumentField(ResourceAttribute))
