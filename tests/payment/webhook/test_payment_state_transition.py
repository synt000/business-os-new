def test_webhook_module_import():
    from src.domains.payment.webhook.service import (
        handle_payment_completed_webhook
    )

    assert handle_payment_completed_webhook is not None
