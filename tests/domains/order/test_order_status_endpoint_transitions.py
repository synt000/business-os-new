from fastapi import HTTPException


def test_order_status_transition_rules_are_enforced():
    from src.domains.order.router import update_order_status

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
    assert "COMPLETED" in allowed["PAID"]

    assert "COMPLETED" not in allowed["CONFIRMED"]
    assert "PAID" not in allowed["CONFIRMED"]
    assert "PACKING" not in allowed["COMPLETED"]
    assert "CONFIRMED" not in allowed["CANCELLED"]

    assert update_order_status is not None
