from dataclasses import dataclass

from src.core.context.tenant_context import TenantContext


@dataclass(frozen=True)
class ChannelResolutionRequest:
    """
    Incoming external channel identity.

    No database logic.
    No tenant lookup logic.
    """

    provider: str
    external_channel_id: str
    verification_token: str | None = None


@dataclass(frozen=True)
class ChannelResolutionResult:
    """
    Channel resolution result.

    Returns resolved tenant context
    or failure information.
    """

    tenant_context: TenantContext | None = None
    resolved: bool = False
    message: str | None = None
