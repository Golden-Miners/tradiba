from fastapi import Request
from fastapi.responses import JSONResponse
import uuid


class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


async def api_error_handler(request: Request, exc: APIError):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "correlation_id": correlation_id
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "correlation_id": correlation_id
        }
    )
