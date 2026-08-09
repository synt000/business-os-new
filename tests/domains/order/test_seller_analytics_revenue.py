from src.models.saas_core import Tenant
from datetime import datetime, timedelta

from src.models.saas_core import Invoice, Order, Payment


def test_seller_revenue_uses_completed_payments_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_revenue_summary,
    )

    now = datetime.utcnow()

    order = Order(
        order_number="ANALYTICS-001",
        platform_channel="SYSTEM",
        customer_name="Analytics Customer",
        tenant_id=tenant_id,
        total_amount=100.0,
        order_status="PAID",
        created_at=now,
    )

    db_session.add(order)
    db_session.flush()

    invoice = Invoice(
        invoice_number="ANALYTICS-INV-001",
        amount=100.0,
        status="PAID",
        order_id=order.id,
        tenant_id=tenant_id,
        created_at=now,
    )

    db_session.add(invoice)
    db_session.flush()

    completed_payment = Payment(
        payment_number="ANALYTICS-PAY-001",
        amount=100.0,
        payment_method="TEST",
        status="COMPLETED",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
        created_at=now,
    )

    pending_payment = Payment(
        payment_number="ANALYTICS-PAY-002",
        amount=50.0,
        payment_method="TEST",
        status="PENDING",
        invoice_id=invoice.id,
        tenant_id=tenant_id,
        created_at=now,
    )

    db_session.add_all([
        completed_payment,
        pending_payment,
    ])
    db_session.commit()

    result = get_revenue_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=now - timedelta(days=1),
        end_at=now + timedelta(days=1),
    )

    assert result["revenue"] == 100.0
    assert result["payment_count"] == 1


def test_seller_daily_revenue_breakdown(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_revenue,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    order = Order(
        order_number="ANALYTICS-DAILY-001",
        platform_channel="SYSTEM",
        customer_name="Daily Analytics Customer",
        tenant_id=tenant_id,
        total_amount=300.0,
        order_status="PAID",
        created_at=base,
    )

    db_session.add(order)
    db_session.flush()

    invoice = Invoice(
        invoice_number="ANALYTICS-DAILY-INV-001",
        amount=300.0,
        status="PAID",
        order_id=order.id,
        tenant_id=tenant_id,
        created_at=base,
    )

    db_session.add(invoice)
    db_session.flush()

    db_session.add_all([
        Payment(
            payment_number="ANALYTICS-DAILY-PAY-001",
            amount=100.0,
            payment_method="TEST",
            status="COMPLETED",
            invoice_id=invoice.id,
            tenant_id=tenant_id,
            created_at=base,
        ),
        Payment(
            payment_number="ANALYTICS-DAILY-PAY-002",
            amount=200.0,
            payment_method="TEST",
            status="COMPLETED",
            invoice_id=invoice.id,
            tenant_id=tenant_id,
            created_at=base + timedelta(days=1),
        ),
    ])

    db_session.commit()

    result = get_daily_revenue(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 12),
    )

    assert result == [
        {"date": "2026-01-10", "revenue": 100.0},
        {"date": "2026-01-11", "revenue": 200.0},
    ]


def test_seller_revenue_endpoint_returns_summary(
    db_session,
    tenant_id,
):
    from fastapi import HTTPException
    from src.domains.dashboard.router import seller_revenue_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_revenue_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "revenue" in result
    assert "payment_count" in result


def test_seller_revenue_endpoint_returns_daily_revenue(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_revenue_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_revenue_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "revenue" in result
    assert "payment_count" in result
    assert "daily_revenue" in result
    assert isinstance(result["daily_revenue"], list)


def test_seller_order_summary_uses_paid_orders_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_order_summary,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-ORDER-001",
            platform_channel="SYSTEM",
            customer_name="Customer 1",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-ORDER-002",
            platform_channel="SYSTEM",
            customer_name="Customer 2",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-ORDER-003",
            platform_channel="SYSTEM",
            customer_name="Customer 3",
            tenant_id=tenant_id,
            total_amount=500.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 11),
    )

    assert result["order_count"] == 2
    assert result["order_value"] == 300.0
    assert result["average_order_value"] == 150.0


def test_seller_daily_order_summary_uses_paid_orders_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_order_summary,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-DAILY-ORDER-001",
            platform_channel="SYSTEM",
            customer_name="Customer 1",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-DAILY-ORDER-002",
            platform_channel="SYSTEM",
            customer_name="Customer 2",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(days=1),
        ),
        Order(
            order_number="ANALYTICS-DAILY-ORDER-003",
            platform_channel="SYSTEM",
            customer_name="Customer 3",
            tenant_id=tenant_id,
            total_amount=500.0,
            order_status="PENDING",
            created_at=base + timedelta(days=1),
        ),
    ])

    db_session.commit()

    result = get_daily_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 12),
    )

    assert result == [
        {
            "date": "2026-01-10",
            "order_count": 1,
            "order_value": 100.0,
            "average_order_value": 100.0,
        },
        {
            "date": "2026-01-11",
            "order_count": 1,
            "order_value": 200.0,
            "average_order_value": 200.0,
        },
    ]

def test_seller_daily_order_summary_uses_paid_orders_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_order_summary,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-DAILY-ORDER-001",
            platform_channel="SYSTEM",
            customer_name="Customer 1",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-DAILY-ORDER-002",
            platform_channel="SYSTEM",
            customer_name="Customer 2",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(days=1),
        ),
        Order(
            order_number="ANALYTICS-DAILY-ORDER-003",
            platform_channel="SYSTEM",
            customer_name="Customer 3",
            tenant_id=tenant_id,
            total_amount=500.0,
            order_status="PENDING",
            created_at=base + timedelta(days=1),
        ),
    ])

    db_session.commit()

    result = get_daily_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 12),
    )

    assert result == [
        {
            "date": "2026-01-10",
            "order_count": 1,
            "order_value": 100.0,
            "average_order_value": 100.0,
        },
        {
            "date": "2026-01-11",
            "order_count": 1,
            "order_value": 200.0,
            "average_order_value": 200.0,
        },
    ]


def test_seller_order_summary_endpoint_returns_summary(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "order_count" in result
    assert "order_value" in result
    assert "average_order_value" in result


def test_seller_order_summary_endpoint_returns_daily_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "daily_orders" in result
    assert isinstance(result["daily_orders"], list)

def test_seller_customer_count_uses_paid_orders_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-CUSTOMER-001",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-002",
            platform_channel="SYSTEM",
            customer_name="Customer B",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-003",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=150.0,
            order_status="PAID",
            created_at=base + timedelta(hours=2),
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-004",
            platform_channel="SYSTEM",
            customer_name="Customer C",
            tenant_id=tenant_id,
            total_amount=500.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=3),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 11),
    )

    assert result == 2


def test_seller_customer_count_ignores_unpaid_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-CUSTOMER-001",
            platform_channel="SYSTEM",
            customer_name="Customer Paid",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-002",
            platform_channel="SYSTEM",
            customer_name="Customer Paid",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-003",
            platform_channel="SYSTEM",
            customer_name="Customer Pending",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 11),
    )

    assert result == 1


def test_seller_customer_count_counts_distinct_paid_customers(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 12, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-DISTINCT-001",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-DISTINCT-002",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=150.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-DISTINCT-003",
            platform_channel="SYSTEM",
            customer_name="Customer B",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 12),
        end_at=datetime(2026, 1, 13),
    )

    assert result == 2


def test_seller_customer_count_is_tenant_scoped(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 14, 10, 0, 0)

    other_tenant = Tenant(
        id="other-analytics-tenant",
        company_name="Other Company",
        owner_email="other@example.com",
    )
    db_session.add(other_tenant)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-TENANT-001",
            platform_channel="SYSTEM",
            customer_name="Shared Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-TENANT-002",
            platform_channel="SYSTEM",
            customer_name="Other Customer",
            tenant_id=other_tenant.id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 14),
        end_at=datetime(2026, 1, 15),
    )

    assert result == 1


def test_seller_customer_count_ignores_unpaid_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 15, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-CUSTOMER-PAID",
            platform_channel="SYSTEM",
            customer_name="Paid Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-PENDING",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-CANCELLED",
            platform_channel="SYSTEM",
            customer_name="Cancelled Customer",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="CANCELLED",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 15),
        end_at=datetime(2026, 1, 16),
    )

    assert result == 1

def test_seller_customer_count_ignores_duplicate_paid_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 15, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-CUSTOMER-001",
            platform_channel="SYSTEM",
            customer_name="Same Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-002",
            platform_channel="SYSTEM",
            customer_name="Same Customer",
            tenant_id=tenant_id,
            total_amount=150.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-003",
            platform_channel="SYSTEM",
            customer_name="Another Customer",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 15),
        end_at=datetime(2026, 1, 16),
    )

    assert result == 2

def test_seller_customer_count_ignores_pending_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_customer_count,
    )

    base = datetime(2026, 1, 20, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="ANALYTICS-CUSTOMER-PAID-001",
            platform_channel="SYSTEM",
            customer_name="Paid Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="ANALYTICS-CUSTOMER-PENDING-001",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=1),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 20),
        end_at=datetime(2026, 1, 21),
    )

    assert result == 1

def test_seller_order_summary_endpoint_returns_customer_count(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "order_count" in result
    assert "order_value" in result
    assert "average_order_value" in result
    assert "customer_count" in result

def test_seller_order_summary_endpoint_returns_customer_count(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "order_count" in result
    assert "order_value" in result
    assert "average_order_value" in result
    assert "customer_count" in result

def test_seller_order_summary_endpoint_returns_customer_average_order_value(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert "customer_count" in result
    assert "average_order_value" in result
    assert isinstance(result["customer_count"], int)
    assert isinstance(result["average_order_value"], (int, float))

def test_seller_customer_count_ignores_pending_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import get_customer_count
    from src.models.saas_core import Order

    base = datetime(2026, 1, 10, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="CUSTOMER-COUNT-PAID",
            platform_channel="SYSTEM",
            customer_name="Paid Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="CUSTOMER-COUNT-PENDING",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=1),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 10),
        end_at=datetime(2026, 1, 11),
    )

    assert result == 1

def test_seller_customer_count_counts_unique_customers_only(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import get_customer_count
    from src.models.saas_core import Order

    base = datetime(2026, 1, 12, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="UNIQUE-CUSTOMER-1",
            platform_channel="SYSTEM",
            customer_name="Repeat Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="UNIQUE-CUSTOMER-2",
            platform_channel="SYSTEM",
            customer_name="Repeat Customer",
            tenant_id=tenant_id,
            total_amount=150.0,
            order_status="PAID",
            created_at=base + timedelta(hours=2),
        ),
        Order(
            order_number="UNIQUE-CUSTOMER-3",
            platform_channel="SYSTEM",
            customer_name="Another Customer",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=base + timedelta(hours=4),
        ),
    ])

    db_session.commit()

    result = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 12),
        end_at=datetime(2026, 1, 13),
    )

    assert result == 2

def test_seller_order_summary_calculates_average_order_value_from_paid_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import get_order_summary
    from src.models.saas_core import Order

    base = datetime(2026, 1, 13, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="AOV-PAID-1",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="AOV-PAID-2",
            platform_channel="SYSTEM",
            customer_name="Customer B",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="PAID",
            created_at=base + timedelta(hours=1),
        ),
        Order(
            order_number="AOV-PENDING",
            platform_channel="SYSTEM",
            customer_name="Customer C",
            tenant_id=tenant_id,
            total_amount=1000.0,
            order_status="PENDING",
            created_at=base + timedelta(hours=2),
        ),
    ])

    db_session.commit()

    result = get_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 13),
        end_at=datetime(2026, 1, 14),
    )

    assert result["order_count"] == 2
    assert result["order_value"] == 400.0
    assert result["average_order_value"] == 200.0

def test_seller_daily_order_summary_groups_paid_orders_by_day(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_order_summary,
    )
    from src.models.saas_core import Order

    db_session.add_all([
        Order(
            order_number="DAILY-ORDER-1",
            platform_channel="SYSTEM",
            customer_name="Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=datetime(2026, 1, 14, 9, 0, 0),
        ),
        Order(
            order_number="DAILY-ORDER-2",
            platform_channel="SYSTEM",
            customer_name="Customer B",
            tenant_id=tenant_id,
            total_amount=200.0,
            order_status="PAID",
            created_at=datetime(2026, 1, 14, 15, 0, 0),
        ),
        Order(
            order_number="DAILY-ORDER-3",
            platform_channel="SYSTEM",
            customer_name="Customer C",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="PAID",
            created_at=datetime(2026, 1, 15, 10, 0, 0),
        ),
        Order(
            order_number="DAILY-ORDER-PENDING",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=999.0,
            order_status="PENDING",
            created_at=datetime(2026, 1, 14, 18, 0, 0),
        ),
    ])

    db_session.commit()

    result = get_daily_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 14),
        end_at=datetime(2026, 1, 16),
    )

    assert len(result) == 2

    day_14 = next(item for item in result if item["date"] == "2026-01-14")
    day_15 = next(item for item in result if item["date"] == "2026-01-15")

    assert day_14["order_count"] == 2
    assert day_15["order_count"] == 1

def test_seller_daily_order_summary_is_tenant_scoped(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_order_summary,
    )
    from src.models.saas_core import Order

    base = datetime(2026, 1, 16, 10, 0, 0)

    db_session.add_all([
        Order(
            order_number="TENANT-A-DAILY",
            platform_channel="SYSTEM",
            customer_name="Tenant A Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=base,
        ),
        Order(
            order_number="TENANT-B-DAILY",
            platform_channel="SYSTEM",
            customer_name="Tenant B Customer",
            tenant_id="other-tenant",
            total_amount=900.0,
            order_status="PAID",
            created_at=base,
        ),
    ])

    db_session.commit()

    result = get_daily_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 16),
        end_at=datetime(2026, 1, 17),
    )

    assert len(result) == 1
    assert result[0]["order_count"] == 1

def test_seller_order_summary_respects_start_inclusive_end_exclusive_boundary(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_order_summary,
    )
    from src.models.saas_core import Order

    start_at = datetime(2026, 1, 17, 0, 0, 0)
    end_at = datetime(2026, 1, 18, 0, 0, 0)

    db_session.add_all([
        Order(
            order_number="BOUNDARY-START",
            platform_channel="SYSTEM",
            customer_name="Start Customer",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=start_at,
        ),
        Order(
            order_number="BOUNDARY-END",
            platform_channel="SYSTEM",
            customer_name="End Customer",
            tenant_id=tenant_id,
            total_amount=999.0,
            order_status="PAID",
            created_at=end_at,
        ),
    ])

    db_session.commit()

    result = get_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=start_at,
        end_at=end_at,
    )

    assert result["order_count"] == 1
    assert result["order_value"] == 100.0
    assert result["average_order_value"] == 100.0

def test_seller_order_analytics_endpoint_returns_complete_summary_shape(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"

    assert set([
        "status",
        "order_count",
        "order_value",
        "average_order_value",
        "customer_count",
        "daily_orders",
    ]).issubset(result.keys())

    assert isinstance(result["order_count"], int)
    assert isinstance(result["order_value"], (int, float))
    assert isinstance(result["average_order_value"], (int, float))
    assert isinstance(result["customer_count"], int)
    assert isinstance(result["daily_orders"], list)

def test_seller_order_analytics_endpoint_combines_paid_order_metrics(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.router import seller_order_analytics
    from src.models.saas_core import Order

    now = datetime.utcnow()
    start_at = datetime(now.year, now.month, now.day)

    db_session.add_all([
        Order(
            order_number="ENDPOINT-METRIC-1",
            platform_channel="SYSTEM",
            customer_name="Endpoint Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=now - timedelta(minutes=30),
        ),
        Order(
            order_number="ENDPOINT-METRIC-2",
            platform_channel="SYSTEM",
            customer_name="Endpoint Customer B",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="PAID",
            created_at=now - timedelta(minutes=20),
        ),
        Order(
            order_number="ENDPOINT-METRIC-PENDING",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=1000.0,
            order_status="PENDING",
            created_at=now - timedelta(minutes=10),
        ),
    ])

    db_session.commit()

    class DummyUser:
        pass

    DummyUser.tenant_id = tenant_id

    result = seller_order_analytics(
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "SUCCESS"
    assert result["order_count"] == 2
    assert result["order_value"] == 400.0
    assert result["average_order_value"] == 200.0
    assert result["customer_count"] == 2

    assert len(result["daily_orders"]) >= 1
    today = next(
        item for item in result["daily_orders"]
        if item["date"] == start_at.strftime("%Y-%m-%d")
    )
    assert today["order_count"] == 2

def test_seller_order_summary_returns_safe_zero_metrics_when_no_orders(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_order_summary,
        get_customer_count,
    )

    result = get_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 20),
        end_at=datetime(2026, 1, 21),
    )

    customer_count = get_customer_count(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 20),
        end_at=datetime(2026, 1, 21),
    )

    assert result["order_count"] == 0
    assert result["order_value"] == 0.0
    assert result["average_order_value"] == 0.0
    assert customer_count == 0

def test_seller_daily_order_summary_includes_daily_value_and_average(
    db_session,
    tenant_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_daily_order_summary,
    )
    from src.models.saas_core import Order

    db_session.add_all([
        Order(
            order_number="DAILY-VALUE-1",
            platform_channel="SYSTEM",
            customer_name="Daily Customer A",
            tenant_id=tenant_id,
            total_amount=100.0,
            order_status="PAID",
            created_at=datetime(2026, 1, 21, 9, 0, 0),
        ),
        Order(
            order_number="DAILY-VALUE-2",
            platform_channel="SYSTEM",
            customer_name="Daily Customer B",
            tenant_id=tenant_id,
            total_amount=300.0,
            order_status="PAID",
            created_at=datetime(2026, 1, 21, 14, 0, 0),
        ),
        Order(
            order_number="DAILY-VALUE-PENDING",
            platform_channel="SYSTEM",
            customer_name="Pending Customer",
            tenant_id=tenant_id,
            total_amount=1000.0,
            order_status="PENDING",
            created_at=datetime(2026, 1, 21, 16, 0, 0),
        ),
    ])

    db_session.commit()

    result = get_daily_order_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=datetime(2026, 1, 21),
        end_at=datetime(2026, 1, 22),
    )

    assert len(result) == 1

    day = result[0]

    assert day["date"] == "2026-01-21"
    assert day["order_count"] == 2
    assert day["order_value"] == 400.0
    assert day["average_order_value"] == 200.0

def test_seller_revenue_summary_uses_start_inclusive_end_exclusive_boundary(
    db_session,
    tenant_id,
    invoice_id,
):
    from src.domains.dashboard.services.seller_analytics_service import (
        get_revenue_summary,
    )
    from src.models.saas_core import Payment

    start_at = datetime(2026, 1, 22, 0, 0, 0)
    end_at = datetime(2026, 1, 23, 0, 0, 0)

    db_session.add_all([
        Payment(
            payment_number="BOUNDARY-001",
            payment_method="TEST",
            invoice_id=invoice_id,
            tenant_id=tenant_id,
            amount=100.0,
            status="COMPLETED",
            created_at=start_at,
        ),
        Payment(
            payment_number="BOUNDARY-002",
            payment_method="TEST",
            invoice_id=invoice_id,
            tenant_id=tenant_id,
            amount=999.0,
            status="COMPLETED",
            created_at=end_at,
        ),
    ])
    db_session.commit()

    result = get_revenue_summary(
        db=db_session,
        tenant_id=tenant_id,
        start_at=start_at,
        end_at=end_at,
    )

    assert result["revenue"] == 100.0
    assert result["payment_count"] == 1
