import time
import collections
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings

rate_vault = collections.defaultdict(list)

class SecurityInfrastructureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Enforce strict multi-tenant context binding or headers filters natively
        client_ip = request.client.host if request.client else "127.0.0.1"
        current_time = time.time()
        rate_vault[client_ip] = [t for t in rate_vault[client_ip] if current_time - t < 60]
        
        if len(rate_vault[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"status": "FAILURE", "detail": "API_RATE_LIMIT_EXCEEDED: BRUTE_FORCE_GUARD_TRIGGERED"}
            )
        rate_vault[client_ip].append(current_time)

        response = await call_next(request)
        
        # Inject OWASP Standard Hardened Security Headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

def setup_global_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "FAILURE_CONTEXT_BLOCKED", "detail": exc.detail}
        )

    @app.exception_handler(Exception)
    async def general_fallback_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"status": "INTERNAL_SERVER_CRITICAL_FAULT", "detail": "TRANSACTION_PROCESSING_TERMINATED_BY_GUARD"}
        )
