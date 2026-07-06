import time
from fastapi import Request
from core.metrics import REQUEST_COUNT, REQUEST_LATENCY

async def metrics_middleware(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.observe(duration)

    return response
