from contextvars import ContextVar

# Stores current request tenant safely (async-safe)
tenant_context: ContextVar[str] = ContextVar("tenant_id", default=None)

def set_tenant(tenant_id: str):
    tenant_context.set(tenant_id)

def get_tenant():
    return tenant_context.get()
