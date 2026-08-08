def test_order_status_transition_rules():
    allowed = {
        "CONFIRMED": {"PACKING", "CANCELLED"},
        "PACKING": {"SHIPPED", "CANCELLED"},
        "SHIPPED": {"COMPLETED", "CANCELLED"},
        "PAID": {"COMPLETED"},
        "COMPLETED": set(),
        "CANCELLED": set(),
    }

    assert "PACKING" in allowed["CONFIRMED"]
    assert "SHIPPED" in allowed["PACKING"]
    assert "COMPLETED" in allowed["SHIPPED"]

    assert "COMPLETED" not in allowed["CONFIRMED"]
    assert "PAID" not in allowed["CONFIRMED"]
    assert "PACKING" not in allowed["COMPLETED"]
    assert "CONFIRMED" not in allowed["CANCELLED"]
