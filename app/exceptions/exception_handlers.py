

import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)

from app.models.error_model import UncoveredAreaError, UnexpectedGeometryError
from app.models.exception_model import UncoveredAreaException, UnexpectedGeometryException


logger = logging.getLogger(__name__)

async def request_validation_exception_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    body = await request.body()
    query_params = request.query_params._dict
    detail = {"errors": error.errors(), "body": body.decode(), "query_params": query_params}
    logger.error(detail)
    return await _request_validation_exception_handler(request, error)

async def uncovered_area_exception_handler(request: Request, error: UncoveredAreaException):
    error_model = UncoveredAreaError(detail=f"Error in uncovered area: {str(error.uncovered_area.wkt)}")
    body = await request.body()
    query_params = request.query_params._dict
    detail = {"errors": error_model.message, "body": body.decode(), "query_params": query_params}
    logger.error(detail)
    return JSONResponse(
        status_code=error.status_code,
        content=error_model.model_dump()
    )

async def unexpected_geometry_exception_handler(request: Request, error: UnexpectedGeometryException):
    error_model = UnexpectedGeometryError(detail=f"Error in uncovered area: {str(error.intersection)}")
    body = await request.body()
    query_params = request.query_params._dict
    detail = {"errors": error_model.message, "body": body.decode(), "query_params": query_params}
    logger.error(detail)
    return JSONResponse(
        status_code=error.status_code,
        content=error_model.model_dump()
    )