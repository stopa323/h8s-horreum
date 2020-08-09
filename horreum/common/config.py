import configparser
import logging

from os import getenv

LOG = logging.getLogger("main")
CONF = None


def get_config() -> configparser.ConfigParser:
    global CONF

    if not CONF:
        CONF = configparser.ConfigParser()
        CONF.read("../etc/config.ini")
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

    if dynamodb_url := getenv("DYNAMODB_LOCAL_URL"):
        cfg.set("dynamodb", "local_url", dynamodb_url)


def print_config(cfg: configparser.ConfigParser) -> None:
    """TBD."""
    msg_lines = ["Running config:"]
    for _section in cfg.sections():
        msg_lines.append(f"[{_section}]")
        for _key, _val in cfg.items(_section):
            msg_lines.append(f"{_key} = {_val}")
    LOG.info("\n\t".join(msg_lines))
