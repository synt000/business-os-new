from src.domains.subscription.models import (
    SubscriptionPlan,
    SubscriptionPayment,
    Subscription,
)

from src.domains.subscription.service import (
    confirm_subscription_payment,
)

from src.domains.accounting.models import AccountLedger

from src.models.saas_core import Invoice


def test_subscription_payment_e2e(
    db_session,
    tenant_id,
):

    # ==========================
    # CREATE PLAN
    # ==========================

    plan = SubscriptionPlan(
        id="plan-test",
        name="PRO",
        duration_days=30,
        price=1000,
        features_json="{}",
    )

    db_session.add(plan)
    db_session.flush()


    # ==========================
    # CREATE PAYMENT
    # ==========================

    payment = SubscriptionPayment(
        id="sub-payment-test",
        tenant_id=tenant_id,
        subscription_id=None,
        plan_id=plan.id,
        amount=1000,
        status="PENDING",
    )

    db_session.add(payment)
    db_session.flush()


    db_session.commit()


    # ==========================
    # CONFIRM PAYMENT
    # ==========================

    result = confirm_subscription_payment(
        db_session,
        payment.id,
    )


    assert result.status == "PAID"
    assert result.subscription_id is not None


    # ==========================
    # SUBSCRIPTION ASSERTION
    # ==========================

    subscription = (
        db_session.query(Subscription)
        .filter(
            Subscription.id == result.subscription_id
        )
        .first()
    )

    assert subscription is not None
    assert subscription.status == "ACTIVE"


    # ==========================
    # LEDGER ASSERTION
    # ==========================

    ledgers = (
        db_session.query(AccountLedger)
        .filter(
            AccountLedger.reference_id == payment.id
        )
        .all()
    )

    assert len(ledgers) == 2

    heads = {
        x.account_head
        for x in ledgers
    }

    assert "CASH_ASSET" in heads
    assert "SUBSCRIPTION_REVENUE" in heads


    # ==========================
    # INVOICE ASSERTION
    # ==========================

    invoice = (
        db_session.query(Invoice)
        .filter(
            Invoice.subscription_id == subscription.id
        )
        .first()
    )

    assert invoice is not None
    assert invoice.status == "PAID"
    assert invoice.amount == 1000
