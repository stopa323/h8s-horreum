# type: ignore
import uvicorn

from fastapi import FastAPI

from horreum.api.router import terraform
from horreum.api.schema.errors import inject_exception_handlers
from horreum.common.config import get_config, print_config
from horreum.db.utils import inject_table_host

app = FastAPI()
app.include_router(prefix="/v1", router=terraform.router)

inject_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    # Todo: Test DynamoDB responsiveness here?
    cfg = get_config()
    print_config(cfg)

    # Reason why this branch is here and not in __main__ section is that there
    # is a need to run application in container while still using local DB.
    if dynamodb_url := cfg.get("dynamodb", "local_url"):
        inject_table_host(dynamodb_url)


# Note: This code runs only locally. When using container version, bind_host and
#       bind_port are set using uvicorn parameters
if __name__ == "__main__":
    cfg = get_config()

    # Note: When run locally, use local DynamoDB by default
    cfg.set("dynamodb", "local_url", "http://localhost:8000")

    uvicorn.run(app,
                host=cfg.get("app", "bind_host"),
                port=cfg.getint("app", "bind_port"))
