from sqlalchemy.orm import Session

from src.domains.customer.contracts.identity_resolution_contract import (
    IdentityResolutionRequest,
    IdentityResolutionResult,
)

from src.domains.customer.services.identity_runtime_resolver import (
    IdentityRuntimeResolver,
)


class IdentityRuntime:
    """
    Application identity runtime facade.

    Responsibility:
    Application entry point for identity resolution.

    No channel logic.
    No database model logic.
    No customer domain rules.
    """

    @staticmethod
    def resolve(
        db: Session,
        request: IdentityResolutionRequest,
        customer_id: str | None = None,
    ) -> IdentityResolutionResult:
        return IdentityRuntimeResolver.resolve(
            db=db,
            request=request,
            customer_id=customer_id,
        )
