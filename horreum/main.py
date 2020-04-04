import uvicorn
from fastapi import FastAPI

from horreum.common.config import get_config


app = FastAPI()


if __name__ == "__main__":
    cfg = get_config()
    uvicorn.run(app, host=cfg.get("DEFAULT", "bind_host"),
                port=cfg.getint("DEFAULT", "bind_port"))
