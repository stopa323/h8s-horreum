import logging

from horreum.db.terraform import ResourceTemplateDB


LOG = logging.getLogger("main")


def inject_table_host(local_url: str) -> None:
    """Sets host for all tables to local URL.

    :param local_url: Local URL to use when accessing table.
    """
    LOG.warning(f"Using DynamoDB local: {local_url}")
    for table in [ResourceTemplateDB]:
        table.Meta.host = local_url  # type: ignore
