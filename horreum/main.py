# type: ignore
import uvicorn

from fastapi import FastAPI
from mongoengine import connect, disconnect
from os import getenv

from horreum.common.config import get_config
from horreum.common.utils import load_fixtures
from horreum.router import node

app = FastAPI()
app.include_router(node.router)


@app.on_event("startup")
async def startup_event():
    cfg = get_config()

    db_connection_string = getenv("DB_CONNECTION", cfg.get("db", "connection"))
    print(f"Using {db_connection_string} for database connection")
    con = connect(db=cfg.get("db", "db_name"), host=db_connection_string)
    con.server_info()
    print("DB connection OK")

    if getenv("APP_LOAD_FIXTURES", False):
        load_fixtures(cfg.get("fixtures", "path"))


@app.on_event("shutdown")
async def shutdown_event():
    disconnect()
    print("Disconnected from DB")


# Note: This code runs only locally. When using container version, bind_host and
#       bind_port are set using uvicorn parameters
if __name__ == "__main__":
    cfg = get_config()
    uvicorn.run(app,
                host=getenv("APP_BIND_HOST",
                            cfg.get("DEFAULT", "bind_host")),
                port=getenv("APP_BIND_PORT",
                            cfg.getint("DEFAULT", "bind_port")))
