import configparser
import logging

from os import getenv

CONF = None

LOG = logging.getLogger("main")


def get_config() -> configparser.ConfigParser:
    global CONF

    if not CONF:
        CONF = configparser.ConfigParser()
        cfg_filepath = "../etc/config.ini"
        read_files = CONF.read(cfg_filepath)
        if not read_files:
            raise IOError(f"Failed to read {cfg_filepath}")

        cfg_override_with_env(CONF)

    return CONF


def cfg_override_with_env(cfg: configparser.ConfigParser) -> None:
    """Override config.ini with environment variables.

    :param cfg: Parsed config.ini file wrapped into configparser.
    """
    if bind_host := getenv("APP_BIND_HOST"):
        cfg.set("app", "bind_host", bind_host)

    if bind_port := getenv("APP_BIND_PORT"):
        cfg.set("app", "bind_port", bind_port)

    if dynamodb_endpoint_url := getenv("DYNAMODB_ENDPOINT_URL"):
        cfg.set("dynamodb", "endpoint_url", dynamodb_endpoint_url)


def print_config(cfg: configparser.ConfigParser) -> None:
    """TBD."""
    msg_lines = ["Running config:"]
    for _section in cfg.sections():
        msg_lines.append(f"[{_section}]")
        for _key, _val in cfg.items(_section):
            msg_lines.append(f"{_key} = {_val}")

    LOG.info("\n\t".join(msg_lines))
