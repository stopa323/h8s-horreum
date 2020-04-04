import pymongo

from horreum.common.config import get_config

CONF = get_config()
DB = None


def get_client() -> pymongo.MongoClient:
    global DB

    if not DB:
        DB = pymongo.MongoClient(CONF.get("db", "connection"))

    return DB[CONF.get("db", "db_name")]
