import logging

from horreum.db.terraform import ResourceTemplateDB


LOG = logging.getLogger("main")


def inject_table_host(endpoint: str) -> None:
    """Sets host for all tables to given URL.

    :param endpoint: URL to DynamoDB service.
    """
    for table in [ResourceTemplateDB]:
        table.Meta.host = endpoint  # type: ignore
