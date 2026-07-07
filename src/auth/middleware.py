from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import jose
from jose import jwt

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 1. DEFINE PUBLIC BYPASS PATHS (UI and Auth Endpoints)
        public_paths = [
            "/", 
            "/auth/login", 
            "/auth/register", 
            "/docs", 
            "/openapi.json", 
            "/redoc"
        ]
        
        # Allow open access to public endpoints and static assets without token validation
        if path in public_paths or path.startswith("/static"):
            return await call_next(request)

        # 2. ENFORCE STRICT JWT PROTECTION FOR CORE ERP DATA PIPELINES
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Return standard error if credentials are missing on protected nodes
            return Response(content='{"detail": "Not authenticated"}', status_code=401, media_type="application/json")
            
        token = auth_header.split(" ")[1]
        try:
            # Decode token dynamically to extract workspace scope details
            payload = jwt.decode(token, "b1z0s_g10b41_m3g4_saas_p14tf0rm_s3cr3t_k3y_2026", algorithms=["HS256"])
            request.state.tenant_id = payload.get("tenant_id")
            request.state.user_id = payload.get("user_id")
        except Exception:
            return Response(content='{"detail": "Invalid or expired token security signature"}', status_code=401, media_type="application/json")

        return await call_next(request)
