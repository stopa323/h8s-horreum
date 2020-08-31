import pytest

from configparser import ConfigParser
from pytest_mock import mocker

from horreum.db.utils import configure_db


@pytest.fixture()
def cfg_stub():
    cfg = ConfigParser()
    cfg.add_section("dynamodb")
    cfg.set("dynamodb", "local_url", "")
    cfg.set("dynamodb", "region", "")
    return cfg


@pytest.fixture()
def m_inject_local_url(mocker):
    m = mocker.patch("horreum.db.utils.inject_local_url")
    return m


@pytest.fixture()
def m_inject_region(mocker):
    m = mocker.patch("horreum.db.utils.inject_region")
    return m


def test_local_url_is_injected(cfg_stub, m_inject_local_url, m_inject_region):
    cfg_stub.set("dynamodb", "local_url", "http://localhost:8000")

    configure_db(cfg_stub)

    assert m_inject_local_url.call_count == 1
    assert m_inject_region.call_count == 0


def test_region_precedence_over_local_url(
        cfg_stub, m_inject_local_url, m_inject_region):
    cfg_stub.set("dynamodb", "local_url", "http://localhost:8000")
    cfg_stub.set("dynamodb", "region", "eu-west-1")

    configure_db(cfg_stub)

    assert m_inject_local_url.call_count == 0
    assert m_inject_region.call_count == 1


def test_region_is_injected(
        cfg_stub, m_inject_local_url, m_inject_region):
    cfg_stub.set("dynamodb", "region", "eu-west-1")

    configure_db(cfg_stub)

    assert m_inject_local_url.call_count == 0
    assert m_inject_region.call_count == 1


def test_error_is_raised_on_missing_values(
        cfg_stub, m_inject_local_url, m_inject_region):
    with pytest.raises(TypeError):
        configure_db(cfg_stub)

    assert m_inject_local_url.call_count == 0
    assert m_inject_region.call_count == 0
