import uvicorn
from fastapi import FastAPI

from horreum.common.config import get_config
from horreum.router import terraform


app = FastAPI()
app.include_router(terraform.router, prefix="/terraform")


if __name__ == "__main__":
    cfg = get_config()
    uvicorn.run(app, host=cfg.get("DEFAULT", "bind_host"),
                port=cfg.getint("DEFAULT", "bind_port"))
