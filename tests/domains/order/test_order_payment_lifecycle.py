def test_order_payment_lifecycle_states():
    allowed = {
        "CONFIRMED": {"PACKING", "CANCELLED"},
        "PACKING": {"SHIPPED", "CANCELLED"},
        "SHIPPED": {"COMPLETED", "CANCELLED"},
        "PAID": {"COMPLETED"},
        "COMPLETED": set(),
        "CANCELLED": set(),
    }

    assert "PAID" not in allowed["CONFIRMED"]
    assert "PAID" in allowed
    assert "COMPLETED" in allowed["PAID"]

    assert "COMPLETED" not in allowed["CONFIRMED"]
    assert "COMPLETED" not in allowed["CANCELLED"]
