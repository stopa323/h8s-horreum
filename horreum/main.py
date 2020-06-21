import uvicorn

from fastapi import FastAPI
from mongoengine import connect, disconnect

from horreum.common.config import get_config
from horreum.router import node


app = FastAPI()
app.include_router(node.router, prefix="/v1/terraform")


@app.on_event("startup")
async def startup_event():
    cfg = get_config()
    c = connect(db=cfg.get("db", "db_name"), host=cfg.get("db", "connection"))
    c.server_info()
    print("DB connection OK")


@app.on_event("shutdown")
async def shutdown_event():
    disconnect()
    print("Disconnected from DB")


if __name__ == "__main__":
    cfg = get_config()
    uvicorn.run(app, host=cfg.get("DEFAULT", "bind_host"),
                port=cfg.getint("DEFAULT", "bind_port"))
