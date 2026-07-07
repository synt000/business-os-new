from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
import jose
from jose import jwt
import json

class AuthMiddleware:
    """
    Upgraded Advanced ASGI Standard Middleware Configuration 
    to prevent asynchronous template loading streaming faults.
    """
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Only process HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]

        # 1. DEFINE PUBLIC BYPASS PATHS (UI and Auth Endpoints)
        public_paths = [
            "/", 
            "/auth/login", 
            "/auth/register", 
            "/docs", 
            "/openapi.json", 
            "/redoc"
        ]
        
        # Fast-track bypass validation for static and public frontends
        if path in public_paths or path.startswith("/static"):
            await self.app(scope, receive, send)
            return

        # 2. ENFORCE JWT PROTECTION FOR DATA API PIPELINES
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("utf-8")

        if not auth_header or not auth_header.startswith("Bearer "):
            response = Response(content=json.dumps({"detail": "Not authenticated"}), status_code=401, media_type="application/json")
            await response(scope, receive, send)
            return
            
        token = auth_header.split(" ")[1]
        try:
            # Decode signature baseline using global architecture key
            payload = jwt.decode(token, "b1z0s_g10b41_m3g4_saas_p14tf0rm_s3cr3t_k3y_2026", algorithms=["HS256"])
            
            # Inject token credentials dynamically into custom header contexts safely
            scope["tenant_id"] = payload.get("tenant_id")
            scope["user_id"] = payload.get("user_id")
        except Exception:
            response = Response(content=json.dumps({"detail": "Invalid or expired token security signature"}), status_code=401, media_type="application/json")
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
