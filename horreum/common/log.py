import logging.config
import yaml


def set_up_logger() -> None:
    with open("../etc/log.yml", "rt") as f:
        logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)
