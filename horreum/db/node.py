import mongoengine as me

from horreum.db.base import HasId


class PortTemplateObj(me.EmbeddedDocument):
    name = me.StringField()
    kind = me.StringField()
    default_value = me.BooleanField()


class NodeTemplateObj(HasId):
    name = me.StringField()
    description = me.StringField()
    automoton = me.StringField()
    keywords = me.ListField(me.StringField)
    ingress_ports = me.ListField(PortTemplateObj)
    egress_ports = me.ListField(PortTemplateObj)
