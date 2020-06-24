import pytest

from pytest_mock import mocker

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
    assert "../etc/horreum.ini" == current_config.read.call_args[0][0]
