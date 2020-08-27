import configparser
import pytest

from pytest_mock import mocker
from unittest.mock import MagicMock

from horreum.common import config


def test_current_config_is_not_overridden(mocker):
    mocker.patch.object(config, "CONF", "ExistingConfig")
    cfg_parser_mock = mocker.patch("horreum.common.config.configparser")

    current_config = config.get_config()

    assert "ExistingConfig" == current_config
    assert [] == cfg_parser_mock.method_calls


def test_config_is_loaded_when_none(mocker):
    mocker.patch.object(config, "CONF", None)
    mocker.patch.object(config.configparser, "ConfigParser")

    current_config = config.get_config()

    assert 1 == current_config.read.call_count
    assert "../etc/config.ini" == current_config.read.call_args[0][0]


def test_exception_raised_on_invalid_config_path(mocker):
    mocker.patch.object(config, "CONF", None)
    m_cfg = MagicMock()
    m_cfg.read.return_value = []
    m_cfg_cls = mocker.patch.object(config.configparser, "ConfigParser")
    m_cfg_cls.return_value = m_cfg

    with pytest.raises(OSError):
        config.get_config()


@pytest.fixture()
def cfg_stub(request):
    cfg = configparser.ConfigParser()
    cfg.add_section(request.param["section"])
    cfg.set(request.param["section"],
            request.param["key"],
            request.param["val"])
    return cfg, request.param["section"], request.param["key"]


@pytest.fixture()
def env_mock(request, monkeypatch):
    env, val = request.param["env"], request.param["val"]
    monkeypatch.setenv(env, val)
    return val


@pytest.mark.parametrize(
    "cfg_stub,env_mock",
    [
        ({"section": "app", "key": "bind_host", "val": "0.0.0.0"},
         {"env": "APP_BIND_HOST", "val": "1.1.1.1"}),
        ({"section": "app", "key": "bind_port", "val": "5000"},
         {"env": "APP_BIND_PORT", "val": "5001"}),
        ({"section": "dynamodb", "key": "endpoint_url", "val": ""},
         {"env": "DYNAMODB_ENDPOINT_URL", "val": "http://localhost:8000"})
    ],
    indirect=["cfg_stub", "env_mock"]
)
def test_override_app_config_default(cfg_stub, env_mock):
    cfg, section, key = cfg_stub

    config.cfg_override_with_env(cfg)

    assert cfg[section][key] == env_mock
