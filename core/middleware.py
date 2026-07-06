from fastapi import Request
from core.tenant_context import set_tenant

class TenantMiddleware:
    async def __call__(self, request: Request, call_next):

        # 🔥 NO MORE HEADER TRUST FOR TENANT
        response = await call_next(request)
        return response
