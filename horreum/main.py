# type: ignore
import logging

from fastapi import FastAPI

from horreum.api.router import terraform
from horreum.api.schema.errors import inject_exception_handlers
from horreum.common.config import get_config, print_config
from horreum.common.log import set_up_logger
from horreum.db.utils import inject_table_host

app = FastAPI()
app.include_router(prefix="/v1", router=terraform.router)

inject_exception_handlers(app)

LOG = logging.getLogger("main")


@app.on_event("startup")
async def startup_event():
    set_up_logger()

    # Todo: Test DynamoDB responsiveness here?
    cfg = get_config()
    print_config(cfg)

    dynamodb_endpoint_url = cfg.get("dynamodb", "endpoint_url")
    inject_table_host(dynamodb_endpoint_url)


# Note: This code runs only locally. When using container version, bind_host and
#       bind_port are set using uvicorn parameters
if __name__ == "__main__":
    import uvicorn
    cfg = get_config()
    uvicorn.run(app,
                host=cfg.get("app", "bind_host"),
                port=cfg.getint("app", "bind_port"))
