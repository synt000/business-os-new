from src.domains.customer.contracts.identity_contract import IdentityContext
from src.domains.customer.contracts.identity_resolution_contract import (
    TenantContext,
    IdentityResolutionRequest,
    IdentityResolutionResult,
    ResolutionStatus,
)


def test_identity_resolution_contract_creation():

    tenant_context = TenantContext(
        tenant_id="tenant-test"
    )

    identity_context = IdentityContext(
        provider="telegram",
        external_user_id="telegram-123",
        external_chat_id="chat-123",
    )

    request = IdentityResolutionRequest(
        tenant_context=tenant_context,
        identity_context=identity_context,
    )

    result = IdentityResolutionResult(
        status=ResolutionStatus.FOUND,
        customer_identity_id="identity-123",
        customer_id="customer-123",
    )

    assert request.tenant_context.tenant_id == "tenant-test"
    assert request.identity_context.provider == "telegram"

    assert result.status == ResolutionStatus.FOUND
    assert result.customer_id == "customer-123"
