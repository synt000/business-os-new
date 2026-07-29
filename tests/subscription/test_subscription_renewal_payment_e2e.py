from datetime import datetime, timedelta
from types import SimpleNamespace

from src.models.saas_core import Tenant

from src.domains.subscription.service import (
    create_plan,
    create_subscription,
    create_subscription_payment,
    confirm_subscription_payment,
)


def test_subscription_renewal_payment_e2e(db_session):
    tenant_id = "test-tenant"
    plan_id = "plan-test"

    # Create tenant
    tenant = Tenant(
        id=tenant_id,
        company_name="TEST COMPANY",
        owner_email="test@example.com"
    )
    db_session.add(tenant)
    db_session.commit()

    # Create subscription plan
    create_plan(
        db_session,
        SimpleNamespace(
            id=plan_id,
            name="TEST PLAN",
            duration_days=30,
            price=1000,
            features_json="{}"
        )
    )

    # 1. Create ACTIVE subscription
    subscription = create_subscription(
        db_session,
        tenant_id,
        plan_id,
        False
    )

    assert subscription.status == "ACTIVE"

    old_expire_date = subscription.expire_date

    # 2. Expire subscription
    subscription.expire_date = datetime.utcnow() - timedelta(days=1)
    db_session.commit()

    assert subscription.expire_date < datetime.utcnow()

    # 3. Create renewal payment
    payment = create_subscription_payment(
        db_session,
        tenant_id,
        plan_id,
        "CASH",
        "RENEWAL-TEST-001"
    )

    assert payment.status != "PAID"

    # 4. Confirm payment
    paid_payment = confirm_subscription_payment(
        db_session,
        payment.id
    )

    assert paid_payment.status == "PAID"

    # 5. Verify renewal
    db_session.refresh(subscription)

    assert subscription.status == "ACTIVE"
    assert subscription.expire_date > old_expire_date
