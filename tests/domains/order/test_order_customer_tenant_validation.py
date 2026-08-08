from src.models.saas_core import Tenant, Customer
from src.domains.order.services.order_service import create_order


def test_order_accepts_same_tenant_customer(
    db_session,
    tenant_id,
):
    customer = Customer(
        customer_name="Same Tenant Customer",
        tenant_id=tenant_id,
    )
    db_session.add(customer)
    db_session.flush()

    order = create_order(
        db=db_session,
        tenant_id=tenant_id,
        order_number="TEST-CUSTOMER-TENANT-001",
        items=[],
        customer_id=customer.id,
        customer_name=customer.customer_name,
    )

    assert order.id
    assert order.customer_id == customer.id
    assert order.tenant_id == tenant_id


def test_order_rejects_cross_tenant_customer(
    db_session,
    tenant_id,
):
    other_tenant_id = f"{tenant_id}-other"

    other_tenant = Tenant(
        id=other_tenant_id,
        company_name="Other Test Company",
        owner_email="other-test@example.com",
    )
    db_session.add(other_tenant)
    db_session.flush()

    customer = Customer(
        customer_name="Other Tenant Customer",
        tenant_id=other_tenant_id,
    )
    db_session.add(customer)
    db_session.flush()

    try:
        create_order(
            db=db_session,
            tenant_id=tenant_id,
            order_number="TEST-CUSTOMER-TENANT-002",
            items=[],
            customer_id=customer.id,
            customer_name=customer.customer_name,
        )
        assert False, "Expected CUSTOMER_NOT_FOUND"
    except Exception as exc:
        assert str(exc) == "CUSTOMER_NOT_FOUND"

    db_session.rollback()


def test_order_rejects_nonexistent_customer(
    db_session,
    tenant_id,
):
    missing_customer_id = "NON-EXISTENT-CUSTOMER-ID"

    try:
        create_order(
            db=db_session,
            tenant_id=tenant_id,
            order_number="TEST-CUSTOMER-TENANT-003",
            items=[],
            customer_id=missing_customer_id,
            customer_name="Missing Customer",
        )
        assert False, "Expected CUSTOMER_NOT_FOUND"
    except Exception as exc:
        assert str(exc) == "CUSTOMER_NOT_FOUND"

    db_session.rollback()
