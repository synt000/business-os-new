import uuid
import time
from fastapi import Request
from core.logging import logger

async def request_logging_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"request_id={request_id} "
        f"path={request.url.path} "
        f"method={request.method} "
        f"status={response.status_code} "
        f"process_time={process_time}"
    )

    response.headers["X-Request-ID"] = request_id

    return response
