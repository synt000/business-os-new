from fastapi import Response
from starlette.types import ASGIApp, Scope, Receive, Send
import json

from src.config import settings
from src.core.security import verify_access_token


class AuthMiddleware:
    """
    Enterprise JWT Authentication Middleware
    Multi Tenant Security Context Injector
    """

    def __init__(self, app: ASGIApp):
        self.app = app


    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ):

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return


        path = scope["path"]


        public_paths = [
            "/",
            "/auth/login",
            "/auth/register",
            "/api/v4/docs",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/api/v4/health"
        ]


        if (
            path in public_paths
            or path.startswith("/static")
        ):
            await self.app(scope, receive, send)
            return



        headers = dict(scope.get("headers", []))

        auth_header = headers.get(
            b"authorization",
            b""
        ).decode()


        if not auth_header.startswith("Bearer "):

            response = Response(
                content=json.dumps(
                    {
                        "detail": "Authentication required"
                    }
                ),
                status_code=401,
                media_type="application/json"
            )

            await response(
                scope,
                receive,
                send
            )
            return



        token = auth_header.split(" ")[1]


        try:

            payload = verify_access_token(token)

            if payload is None:
                raise JWTError()
            scope["user"] = payload.get("user_id")

            scope["tenant_id"] = payload.get(
                "tenant_id"
            )

            scope["role"] = payload.get(
                "role"
            )


        except JWTError:

            response = Response(
                content=json.dumps(
                    {
                        "detail":
                        "Invalid token"
                    }
                ),
                status_code=401,
                media_type="application/json"
            )

            await response(
                scope,
                receive,
                send
            )

            return


        await self.app(
            scope,
            receive,
            send
        )
