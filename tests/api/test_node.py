import pytest

from fastapi.testclient import TestClient
from mongoengine import connect, disconnect

from horreum.db.node import NodeTemplateObj
from horreum.main import app

# Todo: Consider using factories


@pytest.fixture(scope="class")
def mock_database():
    db = connect("testdb", host="mongomock://localhost")
    yield db
    db.drop_database("testdb")
    db.close()
    disconnect()


@pytest.fixture(scope="class")
def fetch_nodes(mock_database):
    return client.get(PATH)


@pytest.fixture(scope="class")
def db_inject_node(mock_database):
    NodeTemplateObj(name="name1", description="desc1", automoton="_CORE",
                    keywords=[], ingressPorts=[], egressPorts=[]).save()


client = TestClient(app)

PATH = "/templates/nodes"


class TestListNodeTemplatesEmpty:

    def test_response_status_is_200(self, fetch_nodes):
        assert 200 == fetch_nodes.status_code

    def test_response_items_are_present(self, fetch_nodes):
        assert "items" in fetch_nodes.json()

    def test_response_items_content_is_empty(self, fetch_nodes):
        assert [] == fetch_nodes.json()["items"]


class TestListNodeTemplates:

    def test_response_status_is_200(self, db_inject_node, fetch_nodes):
        assert 200 == fetch_nodes.status_code

    def test_response_contains_items(self, db_inject_node, fetch_nodes):
        assert "items" in fetch_nodes.json()

    def test_response_contains_single_item(self, db_inject_node, fetch_nodes):
        assert 1 == len(fetch_nodes.json()["items"])

    def test_response_items_contain_id(self, db_inject_node, fetch_nodes):
        assert "id" in fetch_nodes.json()["items"][0]

    def test_response_items_contain_name(self, db_inject_node, fetch_nodes):
        assert "name" in fetch_nodes.json()["items"][0]

    def test_response_items_contain_description(
            self, db_inject_node, fetch_nodes):
        assert "description" in fetch_nodes.json()["items"][0]

    def test_response_items_contain_keywords(
            self, db_inject_node, fetch_nodes):
        assert "keywords" in fetch_nodes.json()["items"][0]

    def test_response_items_contain_ingress_ports(
            self, db_inject_node, fetch_nodes):
        assert "ingressPorts" in fetch_nodes.json()["items"][0]

    def test_response_items_contain_egress_ports(
            self, db_inject_node, fetch_nodes):
        assert "egressPorts" in fetch_nodes.json()["items"][0]

