from src.domains.payment.webhook.service import process_webhook_event
from src.domains.payment.webhook.event import WebhookEvent


def test_first_webhook_event_processed(db_session):
    event = process_webhook_event(
        db=db_session,
        event_id="evt_001",
        provider="stripe",
    )

    assert event.event_id == "evt_001"
    assert event.provider == "stripe"
    assert event.processed is False

    saved = (
        db_session.query(WebhookEvent)
        .filter(WebhookEvent.event_id == "evt_001")
        .first()
    )

    assert saved is not None
    assert saved.processed is False


def test_duplicate_webhook_event_blocked(db_session):
    first = process_webhook_event(
        db=db_session,
        event_id="evt_duplicate_001",
        provider="stripe",
    )

    assert first.event_id == "evt_duplicate_001"

    second = process_webhook_event(
        db=db_session,
        event_id="evt_duplicate_001",
        provider="stripe",
    )

    assert second["status"] == "duplicate"

    count = (
        db_session.query(WebhookEvent)
        .filter(WebhookEvent.event_id == "evt_duplicate_001")
        .count()
    )

    assert count == 1
