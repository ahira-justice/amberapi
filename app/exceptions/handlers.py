from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette import status
from starlette.responses import JSONResponse

from app.exceptions.app_exceptions import AppDomainException, SystemErrorException
from app.logger.custom_logger import logger


async def validation_exception_handler(request: Request, ex: RequestValidationError) -> JSONResponse:
    errors = {}

    for error in jsonable_encoder(ex.errors()):
        errors[error["loc"][1]] = error["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "UnprocessableEntity",
            "message": "Validation error",
            "errors": errors
        },
    )


async def app_exception_handler(request: Request, ex: AppDomainException) -> JSONResponse:
    return JSONResponse(
        status_code=ex.status_code,
        content={
            "code": ex.code,
            "message": ex.message,
        },
    )


async def exception_handler(request: Request, ex: Exception) -> JSONResponse:
    logger.error(ex)

    ex = SystemErrorException()

    logger.info(f"Response Status Code: {ex.status_code}")

    return JSONResponse(
        status_code=ex.status_code,
        content={
            "code": ex.code,
            "message": ex.message,
        },
    )
