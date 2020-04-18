import mongoengine as me

from uuid import uuid4


class HasId(me.Document):
    id = me.StringField(primary_key=True, required=True,
                        default=lambda: str(uuid4()))

    meta = {"allow_inheritance": True}
