from sqlalchemy.orm import Session

from src.domains.customer.contracts.identity_contract import IdentityContext
from src.domains.customer.services.customer_identity_service import (
    CustomerIdentityService,
)


class IdentityOrchestrationService:
    """
    Identity resolution orchestration layer.

    Responsibility:
    IdentityContext -> CustomerIdentityService

    No channel logic.
    No database model logic.
    """

    @staticmethod
    def resolve(
        db: Session,
        tenant_id: str,
        context: IdentityContext,
        customer_id: str | None = None,
    ):
        existing = CustomerIdentityService.lookup(
            db=db,
            tenant_id=tenant_id,
            provider=context.provider,
            external_user_id=context.external_user_id,
        )

        if existing:
            return existing

        if not customer_id:
            return None

        return CustomerIdentityService.bind(
            db=db,
            tenant_id=tenant_id,
            customer_id=customer_id,
            context=context,
        )
