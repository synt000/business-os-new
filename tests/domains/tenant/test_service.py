import pytest

from src.domains.tenant.service import create_tenant


def test_create_tenant_success(db_session):
    name = "Test Company"

    result = create_tenant(
        db_session,
        name
    )

    assert result.company_name == "Test Company"
    assert result.subscription_tier.value == "FREE_TRIAL"
    assert result.is_billing_active is True
