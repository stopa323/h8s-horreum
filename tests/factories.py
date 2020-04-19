import factory

from horreum.db import terraform


class TerraformResource(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = terraform.Resource

    name = factory.Sequence(lambda n: f"tf_resource-{n}")
