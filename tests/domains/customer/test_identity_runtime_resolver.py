from src.domains.customer.adapters.telegram_identity_adapter import (
    TelegramIdentityAdapter,
)

from src.domains.customer.contracts.identity_resolution_contract import (
    IdentityResolutionRequest,
    TenantContext,
    ResolutionStatus,
)

from src.domains.customer.services.identity_runtime_resolver import (
    IdentityRuntimeResolver,
)

from src.models.saas_core import Customer


def test_identity_runtime_resolver_found(
    db_session,
    tenant_id,
):
    customer = Customer(
        id="customer-runtime-test",
        customer_name="Runtime Test Customer",
        tenant_id=tenant_id,
    )

    db_session.add(customer)
    db_session.commit()

    context = TelegramIdentityAdapter().resolve_identity(
        external_user_id="telegram-runtime-123",
        external_chat_id="chat-runtime-123",
    )

    request = IdentityResolutionRequest(
        tenant_context=TenantContext(
            tenant_id=tenant_id,
        ),
        identity_context=context,
    )

    result = IdentityRuntimeResolver.resolve(
        db=db_session,
        request=request,
        customer_id=customer.id,
    )

    assert result.status == ResolutionStatus.FOUND
    assert result.customer_id == customer.id
