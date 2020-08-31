import logging

from configparser import ConfigParser

from horreum.db.terraform import ResourceTemplateDB


LOG = logging.getLogger("main")


def inject_local_url(endpoint: str) -> None:
    """Sets tables' host to use local DynamoDB.

    :param endpoint: URL to your local DynamoDB service.
    """
    for table in [ResourceTemplateDB]:
        table.Meta.host = endpoint  # type: ignore
    LOG.info(f"Using local DynamoDB: {endpoint}")


def inject_region(region: str) -> None:
    """Sets tables' region to use AWS-managed DynamoDb.

    :param region: AWS region name.
    """
    for table in [ResourceTemplateDB]:
        table.Meta.region = region  # type: ignore
    LOG.info(f"Using DynamoDB in region {region}")


def configure_db(cfg: ConfigParser) -> None:
    """Sets up database configuration.

    :param cfg: ConfigParser instance with loaded configuration file.
    """
    if dynamodb_region := cfg.get("dynamodb", "region"):
        inject_region(dynamodb_region)
    elif dynamodb_local_url := cfg.get("dynamodb", "local_url"):
        inject_local_url(dynamodb_local_url)
    else:
        raise TypeError("Invalid DynamoDB configuration. Either `local_url` or "
                        "`region` must be set.")
