from src.application.identity.runtime import IdentityRuntime

from src.domains.customer.adapters.telegram_identity_adapter import (
    TelegramIdentityAdapter,
)

from src.domains.customer.contracts.identity_resolution_contract import (
    IdentityResolutionRequest,
    TenantContext,
    ResolutionStatus,
)

from src.models.saas_core import Customer


def test_identity_application_runtime_found(
    db_session,
    tenant_id,
):
    customer = Customer(
        id="customer-app-runtime-test",
        customer_name="Application Runtime Test",
        tenant_id=tenant_id,
    )

    db_session.add(customer)
    db_session.commit()

    context = TelegramIdentityAdapter().resolve_identity(
        external_user_id="telegram-app-runtime-123",
        external_chat_id="chat-app-runtime-123",
    )

    request = IdentityResolutionRequest(
        tenant_context=TenantContext(
            tenant_id=tenant_id,
        ),
        identity_context=context,
    )

    result = IdentityRuntime.resolve(
        db=db_session,
        request=request,
        customer_id=customer.id,
    )

    assert result.status == ResolutionStatus.FOUND
    assert result.customer_id == customer.id
