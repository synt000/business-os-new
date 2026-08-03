from sqlalchemy.orm import Session

from src.models.saas_core import Customer, CustomerIdentity
from src.domains.customer.contracts.identity_contract import IdentityContext


class CustomerIdentityService:

    @staticmethod
    def lookup(
        db: Session,
        tenant_id: str,
        provider: str,
        external_user_id: str,
    ):
        return (
            db.query(CustomerIdentity)
            .filter(
                CustomerIdentity.tenant_id == tenant_id,
                CustomerIdentity.provider == provider,
                CustomerIdentity.external_user_id == external_user_id,
            )
            .first()
        )


    @staticmethod
    def bind(
        db: Session,
        tenant_id: str,
        customer_id: str,
        context: IdentityContext | None = None,
        provider: str | None = None,
        external_user_id: str | None = None,
        external_chat_id: str | None = None,
    ):
        if context:
            provider = context.provider
            external_user_id = context.external_user_id
            external_chat_id = context.external_chat_id

        existing = CustomerIdentityService.lookup(
            db,
            tenant_id,
            provider,
            external_user_id,
        )

        if existing:
            return existing

        identity = CustomerIdentity(
            tenant_id=tenant_id,
            customer_id=customer_id,
            provider=provider,
            external_user_id=external_user_id,
            external_chat_id=external_chat_id,
        )

        db.add(identity)
        db.commit()
        db.refresh(identity)

        return identity
