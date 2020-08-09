import pytest

from botocore.exceptions import ClientError
from fastapi.testclient import TestClient
from moto import mock_dynamodb2

from horreum.db.terraform.resource import _ResourceAttribute, ResourceTemplateDB
from horreum.main import app


client = TestClient(app)

GET_PATH = "/v1/terraform/resources"
PUT_PATH_TEMPLATE = "/v1/terraform/resources/{resource_name}"


@pytest.fixture()
def resource_table(aws_credentials):
    with mock_dynamodb2():
        ResourceTemplateDB.create_table(
            read_capacity_units=1, write_capacity_units=1)
        yield


@pytest.fixture()
def single_item_db(resource_table):
    resource = ResourceTemplateDB(name="aws_vpc", attributes=[
        _ResourceAttribute(name="cidr", type="String", is_argument=True,
                           is_required=True)
    ])
    resource.save()
    return resource


def test_query_empty_db(resource_table):
    expected_response = {"terraformResources": []}

    response = client.get(GET_PATH)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_query_populated_db(single_item_db):
    expected_response = {
        "terraformResources": [{
            "name": single_item_db.name,
            "description": single_item_db.description,
            "attributes": [{
                "name": single_item_db.attributes[0].name,
                "description": single_item_db.attributes[0].description,
                "type": single_item_db.attributes[0].type,
                "isArgument": single_item_db.attributes[0].is_argument,
                "isRequired": single_item_db.attributes[0].is_required
            }]}]}

    response = client.get(GET_PATH)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_boto_client_error_on_get(mocker):
    m_scan = mocker.patch.object(ResourceTemplateDB, "scan")
    m_scan.side_effect = ClientError(
        error_response={"Error": {
            "Code": 2137, "Message": "Oh no! What do we do?!"}},
        operation_name="smash")
    expected_response = {
        "message": "Handling unexpected Spanish Inquisition visit. Please try"
                   " again later.",
        "details": "An error occurred (2137) when calling the smash operation: "
                   "Oh no! What do we do?!"}

    response = client.get(GET_PATH)

    assert response.status_code == 500
    assert response.json() == expected_response


PUT_REQ_BODY = {
    "description": "AWS VPC.",
    "attributes": [{
        "name": "cidr",
        "description": "VPC CIDR.",
        "type": "String",
        "isArgument": True,
        "isRequired": True,
    }]
}


def test_put_new_resource(resource_table):
    url = PUT_PATH_TEMPLATE.format(resource_name="aws_vpc")
    expected_response = dict(name="aws_vpc", **PUT_REQ_BODY)

    response = client.put(url=url, json=PUT_REQ_BODY)

    assert response.status_code == 201
    assert response.json() == expected_response


def test_replace_existing_resource(single_item_db):
    url = PUT_PATH_TEMPLATE.format(resource_name="aws_vpc")
    expected_response = dict(name="aws_vpc", **PUT_REQ_BODY)

    response = client.put(url=url, json=PUT_REQ_BODY)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_boto_client_error_on_put(mocker):
    m_scan = mocker.patch.object(ResourceTemplateDB, "get")
    m_scan.side_effect = ClientError(
        error_response={"Error": {
            "Code": 2137, "Message": "Oh no! What do we do?!"}},
        operation_name="smash")

    url = PUT_PATH_TEMPLATE.format(resource_name="aws_vpc")
    expected_response = {
        "message": "Handling unexpected Spanish Inquisition visit. Please try"
                   " again later.",
        "details": "An error occurred (2137) when calling the smash operation: "
                   "Oh no! What do we do?!"}

    response = client.put(url=url, json=PUT_REQ_BODY)

    assert response.status_code == 500
    assert response.json() == expected_response
