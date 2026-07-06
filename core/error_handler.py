from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": str(exc),
            "path": request.url.path
        }
    )
