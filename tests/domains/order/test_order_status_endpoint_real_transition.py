import pytest

from src.domains.order.router import update_order_status
from src.domains.order.schemas import OrderStatusUpdate


class DummyUser:
    tenant_id = "test-tenant"


@pytest.mark.asyncio
async def test_confirmed_cannot_jump_to_completed(
    db_session,
    tenant_id,
):
    from src.models.saas_core import Order

    order = Order(
        order_number="TEST-REAL-TRANSITION-001",
        platform_channel="SYSTEM",
        customer_name="Transition Test",
        tenant_id=tenant_id,
        order_status="CONFIRMED",
    )

    db_session.add(order)
    db_session.flush()

    data = OrderStatusUpdate(status="COMPLETED")

    with pytest.raises(Exception):
        await update_order_status(
            order_id=order.id,
            data=data,
            current_user=DummyUser(),
            db=db_session,
        )
