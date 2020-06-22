import yaml

from glob import glob
from os.path import abspath

from horreum.provider.node import load_node_fixture
from horreum.schema.node import NodeTemplateCreate


def load_fixtures(path: str) -> None:
    """Load template fixtures to database.

    Recursively searches for *.yml files and load them. Invalid or not matching
    files are skipped.

    :param path: Path to directory containing fixture files.
    """
    absolute_path = abspath(path)
    yml_filepaths = glob(f"{absolute_path}/*.yml", recursive=True)
    print(f"Found {len(yml_filepaths)} potential fixture file(s)")

    for filepath in yml_filepaths:
        try:
            with open(filepath, "r") as stream:
                for file_content in yaml.safe_load_all(stream):
                    node_create_obj = NodeTemplateCreate(**file_content)
                    load_node_fixture(node_create_obj)
        except (OSError, yaml.YAMLError) as err:
            print(f"Skipping fixture ({filepath}) due to: {err}")
            continue
        else:
            print(f"Loaded fixture(s) from {filepath}")
