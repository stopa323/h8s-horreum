import mongoengine as me

from horreum.db.base import HasId


class PortTemplateObj(me.EmbeddedDocument):
    name = me.StringField()
    kind = me.StringField()
    hasDefault = me.BooleanField(default=False)
    defaultValue = me.StringField(default=None)

    meta = {"allow_inheritance": True}


class NodeTemplateObj(HasId):
    name = me.StringField()
    description = me.StringField()
    automoton = me.StringField()
    keywords = me.SortedListField(me.StringField())
    ingressPorts = me.EmbeddedDocumentListField(PortTemplateObj)
    egressPorts = me.EmbeddedDocumentListField(PortTemplateObj)
