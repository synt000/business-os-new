from dataclasses import dataclass
from enum import Enum

from src.domains.customer.contracts.identity_contract import IdentityContext
from src.core.context.tenant_context import TenantContext


class ResolutionStatus(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    BIND_REQUIRED = "BIND_REQUIRED"
    REJECTED = "REJECTED"


@dataclass
class IdentityResolutionRequest:
    tenant_context: TenantContext
    identity_context: IdentityContext


@dataclass
class IdentityResolutionResult:
    status: ResolutionStatus
    customer_identity_id: str | None = None
    customer_id: str | None = None
    message: str | None = None
