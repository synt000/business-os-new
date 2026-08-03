from src.domains.customer.adapters.telegram_identity_adapter import (
    TelegramIdentityAdapter,
)
from src.domains.customer.services.identity_orchestration_service import (
    IdentityOrchestrationService,
)
from src.models.saas_core import Customer


def test_identity_orchestration_bind(
    db_session,
    tenant_id,
):
    customer = Customer(
        id="customer-identity-test",
        customer_name="Identity Test Customer",
        tenant_id=tenant_id,
    )

    db_session.add(customer)
    db_session.commit()

    context = TelegramIdentityAdapter().resolve_identity(
        external_user_id="telegram-12345",
        external_chat_id="chat-12345",
    )

    result = IdentityOrchestrationService.resolve(
        db=db_session,
        tenant_id=tenant_id,
        context=context,
        customer_id=customer.id,
    )

    assert result is not None
    assert result.provider == "telegram"
    assert result.external_user_id == "telegram-12345"
    assert result.customer_id == customer.id
