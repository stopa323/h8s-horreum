from botocore.exceptions import ClientError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class InternalError(BaseModel):
    message: str = Field(..., title="Error message.")
    details: str = Field(..., title="Error details.")


def inject_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ClientError, dynamodb_exception_handler)


async def dynamodb_exception_handler(request: Request, exc: ClientError) \
        -> JSONResponse:
    # Todo: Define some structure for debug info e.g.
    #       https://cloud.google.com/apis/design/errors#generating_errors
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=InternalError(message="Handling unexpected Spanish Inquisition "
                                      "visit. Please try again later.",
                              details=str(exc)).dict())
    return response
