import pytest

from src.domains.order.router import update_order_status
from src.domains.order.schemas import OrderStatusUpdate


class DummyUser:
    tenant_id = "test-tenant"


@pytest.mark.asyncio
async def test_paid_can_transition_to_completed(
    db_session,
    tenant_id,
):
    from src.models.saas_core import Order

    order = Order(
        order_number="TEST-PAID-COMPLETE-001",
        platform_channel="SYSTEM",
        customer_name="Paid Transition Test",
        tenant_id=tenant_id,
        order_status="PAID",
    )

    db_session.add(order)
    db_session.flush()

    data = OrderStatusUpdate(status="COMPLETED")

    result = await update_order_status(
        order_id=order.id,
        data=data,
        current_user=DummyUser(),
        db=db_session,
    )

    assert result["status"] == "COMPLETED"
    assert order.order_status == "COMPLETED"
