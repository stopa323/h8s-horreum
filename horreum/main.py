# type: ignore
import argparse
import uvicorn

from fastapi import FastAPI
from mongoengine import connect, disconnect

from horreum.common.config import get_config
from horreum.common.utils import load_fixtures
from horreum.router import node

parser = argparse.ArgumentParser(description="h8s-horreum app")
parser.add_argument("--load-fixtures", action="store_true",
                    dest="load_fixtures", default=False,
                    help="Loads template fixtures when True")

app = FastAPI()
app.include_router(node.router)


@app.on_event("startup")
async def startup_event():
    cfg = get_config()
    con = connect(db=cfg.get("db", "db_name"), host=cfg.get("db", "connection"))
    con.server_info()
    print("DB connection OK")

    args = parser.parse_args()
    if args.load_fixtures:
        load_fixtures(cfg.get("fixtures", "path"))


@app.on_event("shutdown")
async def shutdown_event():
    disconnect()
    print("Disconnected from DB")


if __name__ == "__main__":
    cfg = get_config()
    uvicorn.run(app, host=cfg.get("DEFAULT", "bind_host"),
                port=cfg.getint("DEFAULT", "bind_port"))
