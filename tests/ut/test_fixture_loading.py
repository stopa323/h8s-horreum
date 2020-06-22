import pytest

from mongoengine import connect, disconnect
from pytest_mock import mocker

from horreum.common.utils import load_fixtures
from horreum.db.node import NodeTemplateObj
from horreum.schema.node import NodeTemplateCreate
from horreum.provider.node import load_node_fixture


@pytest.fixture()
def mock_database():
    db = connect("testdb", host="mongomock://localhost")
    yield db
    db.drop_database("testdb")
    db.close()
    disconnect()


@pytest.fixture()
def insert_fixture(mock_database):
    NodeTemplateObj(name="node-1", automoton="automoton-1",
                    description="Do not override").save()


def test_fixture_loaded(mock_database):
    node_fixture = NodeTemplateCreate(name="node-1", automoton="automoton-1")

    load_node_fixture(node_fixture)

    assert 1 == len(NodeTemplateObj.objects)

    node_db = NodeTemplateObj.objects[0]
    assert "node-1" == node_db.name
    assert "" == node_db.description
    assert "automoton-1" == node_db.automoton
    assert [] == node_db.keywords
    assert [] == node_db.ingressPorts
    assert [] == node_db.egressPorts


def test_fixture_not_loaded_when_duplicated(insert_fixture):
    node_fixture = NodeTemplateCreate(name="node-1", automoton="automoton-1",
                                      description="OVERRIDING...")

    load_node_fixture(node_fixture)

    assert 1 == len(NodeTemplateObj.objects)

    node_db = NodeTemplateObj.objects[0]
    assert "OVERRIDING..." != node_db.description == "Do not override"


def test_placeholder1(mocker):
    glob_mock = mocker.patch("horreum.common.utils.glob")
    glob_mock.return_value = []

    open_mock = mocker.patch("builtins.open")

    yaml_mock = mocker.patch("horreum.common.utils.yaml")
    yaml_mock.safe_load_all.return_value = []

    load_fixtures("../some/path")

    assert 0 == open_mock.call_count
    assert 0 == yaml_mock.call_count


def test_placeholder2(mocker):
    glob_mock = mocker.patch("horreum.common.utils.glob")
    glob_mock.return_value = ["file001.yml"]

    open_mock = mocker.patch("builtins.open")

    yaml_mock = mocker.patch("horreum.common.utils.yaml")
    yaml_mock.safe_load_all.return_value = []

    load_fixtures("../some/path")

    assert 1 == open_mock.call_count
    assert 0 == yaml_mock.call_count
