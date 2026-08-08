def test_order_status_can_be_updated(
    db_session,
    tenant_id,
):
    from src.models.saas_core import Order

    order = Order(
        order_number="TEST-STATUS-001",
        platform_channel="SYSTEM",
        customer_name="Status Test",
        tenant_id=tenant_id,
        order_status="CONFIRMED",
    )

    db_session.add(order)
    db_session.flush()

    assert order.order_status == "CONFIRMED"

    order.order_status = "PACKING"
    db_session.flush()

    assert order.order_status == "PACKING"
