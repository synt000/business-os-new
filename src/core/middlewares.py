import time
import uuid
import collections

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import settings


# ==========================================
# RATE LIMIT SECURITY VAULT
# ==========================================

rate_vault = collections.defaultdict(list)


# ==========================================
# BLOCKED PATH SECURITY
# ==========================================

BLOCKED_PATHS = [
    "/.env",
    "/.git",
    "/config.py",
    "/database.db",
    "/businessos.db",
    "/secret",
    "/backup"
]


# ==========================================
# SECURITY INFRASTRUCTURE MIDDLEWARE
# ==========================================

class SecurityInfrastructureMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        request_id = str(uuid.uuid4())


        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )


        user_agent = request.headers.get(
            "user-agent",
            "unknown"
        )


        path = request.url.path.lower()



        # ----------------------------------
        # PATH TRAVERSAL PROTECTION
        # ----------------------------------

        for blocked in BLOCKED_PATHS:

            if blocked in path:

                return JSONResponse(
                    status_code=403,
                    content={
                        "status":"BLOCKED",
                        "detail":"SECURITY_POLICY_VIOLATION",
                        "request_id":request_id
                    }
                )



        # ----------------------------------
        # BASIC BOT SCANNER BLOCK
        # ----------------------------------

        suspicious_agents = [
            "sqlmap",
            "nikto",
            "nmap",
            "masscan",
            "acunetix"
        ]


        for agent in suspicious_agents:

            if agent in user_agent.lower():

                return JSONResponse(
                    status_code=403,
                    content={
                        "status":"BLOCKED",
                        "detail":"MALICIOUS_SCANNER_DETECTED",
                        "request_id":request_id
                    }
                )



        # ----------------------------------
        # RATE LIMIT
        # ----------------------------------

        now = time.time()


        rate_vault[client_ip] = [
            t for t in rate_vault[client_ip]
            if now - t < 60
        ]


        if len(rate_vault[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:

            return JSONResponse(
                status_code=429,
                content={
                    "status":"BLOCKED",
                    "detail":"RATE_LIMIT_EXCEEDED",
                    "request_id":request_id
                }
            )


        rate_vault[client_ip].append(now)



        response = await call_next(request)



        # ----------------------------------
        # SECURITY HEADERS
        # ----------------------------------

        response.headers["X-Request-ID"] = request_id

        response.headers["X-Frame-Options"] = "DENY"

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"


        response.headers[
            "X-XSS-Protection"
        ] = "1; mode=block"


        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; includeSubDomains"
        )


        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"


        return response



# ==========================================
# GLOBAL EXCEPTION CONTROL
# ==========================================

def setup_global_exception_handlers(app):


    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request:Request,
        exc:HTTPException
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status":"FAILURE",
                "detail":exc.detail
            }
        )


    @app.exception_handler(Exception)
    async def global_exception_handler(
        request:Request,
        exc:Exception
    ):
        import traceback
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "status":"INTERNAL_SERVER_ERROR",
                "detail":str(exc)
            }
        )
