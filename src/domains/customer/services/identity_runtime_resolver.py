from sqlalchemy.orm import Session

from src.domains.customer.contracts.identity_resolution_contract import (
    IdentityResolutionRequest,
    IdentityResolutionResult,
    ResolutionStatus,
)

from src.domains.customer.services.identity_orchestration_service import (
    IdentityOrchestrationService,
)


class IdentityRuntimeResolver:
    """
    Runtime identity resolution boundary.

    Responsibility:
    IdentityResolutionRequest
        ->
    IdentityResolutionResult

    No channel logic.
    No database model logic.
    """

    @staticmethod
    def resolve(
        db: Session,
        request: IdentityResolutionRequest,
        customer_id: str | None = None,
    ) -> IdentityResolutionResult:

        identity = IdentityOrchestrationService.resolve(
            db=db,
            tenant_id=request.tenant_context.tenant_id,
            context=request.identity_context,
            customer_id=customer_id,
        )

        if identity:
            return IdentityResolutionResult(
                status=ResolutionStatus.FOUND,
                customer_identity_id=identity.id,
                customer_id=identity.customer_id,
            )

        if customer_id:
            return IdentityResolutionResult(
                status=ResolutionStatus.BIND_REQUIRED,
                customer_id=customer_id,
            )

        return IdentityResolutionResult(
            status=ResolutionStatus.NOT_FOUND,
        )
