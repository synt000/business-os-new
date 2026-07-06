from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from src.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        public_paths = [
            "/",
            "/auth/login",
            "/auth/register",
            "/health",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
        ]

        # Public path ဖြစ်ရင် Token မစစ်တော့ဘဲ တန်းလွှတ်လိုက်မယ်
        if request.url.path in public_paths:
            return await call_next(request)

        # Authorization Header ရှိမရှိ စစ်မယ်
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid token"
            )

        # Token ကို ခွဲထုတ်ပြီး decode လုပ်မယ်
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            request.state.user = payload.get("sub")
            request.state.tenant_id = payload.get("tenant_id")

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return await call_next(request)
