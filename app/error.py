from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from app.dependencies import config


async def exception_handler(request: Request, e: Exception) -> JSONResponse:
    if config.debug:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "type": e.__class__.__name__,
                    "exc": str(e)
                }
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": False,
                "error": "Internal Server Error"
            }
        )


async def http_exception_handler(request: Request, e: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=e.status_code,
        content={
            "status": False,
            "error": e.detail
        }
    )
