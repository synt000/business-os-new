from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    """
    Runtime tenant boundary context.

    Responsibility:
    Carry resolved tenant identity across application runtime.

    No database access.
    No tenant lookup logic.
    """

    tenant_id: str
