from pydantic import BaseModel

from app.models.enums import ErrorCodes


class ErrorResponse(BaseModel):
    detail: str

class UncoveredAreaError(ErrorResponse):
    message: str = "Uncovered area detected."
    code: ErrorCodes = ErrorCodes.UNCOVERED_AREA_ERROR

class UnexpectedGeometryError(ErrorResponse):
    message: str = "Unexpected geometry type in intersection."
    code: ErrorCodes = ErrorCodes.GEOMETRY_ERROR

class UnexpectedErrorResponse(ErrorResponse):
    message: str = "An unexpected error occurred."
    code: ErrorCodes = ErrorCodes.SYSTEM_ERROR

error_responses_400 = {
    400: {
        "model": UnexpectedGeometryError,
        "description": "Invalid geometry"
    },
}

error_responses_500 = {
    500: {
        "model": UnexpectedErrorResponse,
        "description": "An unexpected error occurred."
    },
}