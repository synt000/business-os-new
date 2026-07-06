from fastapi import Request
import time
import uuid
from core.logging import logger

async def telemetry_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"[TRACE] request_id={request_id} "
        f"path={request.url.path} "
        f"method={request.method} "
        f"status={response.status_code} "
        f"duration={round(duration, 4)}s"
    )

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = str(duration)

    return response
