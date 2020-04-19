from tests import factories, utils

from horreum.provider import terraform


class ListResourcesTestCase(utils.DBMock):

    def test_no_objects(self):
        response = terraform.list_resources()

        self.assertListEqual([], response)

    def test_response_object(self):
        obj = factories.TerraformResource()

        response = terraform.list_resources()

        self.assertListEqual([obj], response)
