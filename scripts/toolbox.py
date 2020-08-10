import argparse
import sys
import os

from pathlib import Path
from requests import exceptions, put
from yaml import safe_load_all

cli = argparse.ArgumentParser(description="Useful set of operations that are "
                                          "not part of application.")
cli.add_argument(
    "--create-db-tables",
    action="store_true",
    default=False,
    help="Use to ensure all tables are present in local DynamoDB")
cli.add_argument(
    "--tf-fixture-file",
    action="store",
    default=None,
    help="Path to file containing fixtures for Terraform resource templates.")


def create_db_tables():
    """Ensures all specified tables are present in local DynamoDB instance."""
    # Append current dir to path so that `horreum` package is visible to python
    sys.path.append(os.getcwd())

    from horreum.db.terraform import ResourceTemplateDB

    TABLE_LIST = [ResourceTemplateDB]
    DYNAMODB_URL = "http://localhost:8000"

    for table in TABLE_LIST:
        table.Meta.host = DYNAMODB_URL
        if table.exists():
            print(f"[SKIP]\tTable `{table.Meta.table_name}` already exists")
            continue

        table.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        print(f"[OK]\tTable `{table.Meta.table_name}` created")


def load_tf_resource_fixtures(filepath: str):
    path = Path(filepath)
    with open(path.absolute(), "r") as fs:
        for resource_tmpl in safe_load_all(fs):
            resource_name = resource_tmpl.pop("name")
            url = f"http://localhost:8003/v1/terraform/resources/{resource_name}"
            res = put(url=url, json=resource_tmpl)

            try:
                res.raise_for_status()
            except exceptions.HTTPError:
                print(f"[ERR] Could not register resource {resource_name}:\n"
                      f"{res.json()}")


if __name__ == "__main__":
    args = cli.parse_args()

    if args.create_db_tables:
        create_db_tables()

    if args.tf_fixture_file:
        load_tf_resource_fixtures(args.tf_fixture_file)