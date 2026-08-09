from datetime import datetime, timedelta

from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.execution_models import CampaignExecutionLog
from src.domains.campaign.services.scheduler_service import process_retry_campaigns
from src.domains.social_center.models import SocialChannel


def test_campaign_retry_failure_becomes_success(
    db_session,
    tenant_id,
    monkeypatch,
):
    channel = SocialChannel(
        id="retry-telegram-channel",
        tenant_id=tenant_id,
        platform="telegram",
        channel_name="Retry Telegram",
        external_id="retry-chat-001",
        access_token="test-token",
        webhook_token="test-webhook",
        is_active=True,
    )
    db_session.add(channel)

    campaign = Campaign(
        id="retry-success-campaign",
        tenant_id=tenant_id,
        name="Retry Success Campaign",
        content="Retry content",
        status="scheduled",
        is_active=True,
    )
    db_session.add(campaign)

    db_session.add(
        CampaignChannel(
            id="retry-success-campaign-channel",
            campaign_id=campaign.id,
            channel_id=channel.id,
        )
    )

    execution = CampaignExecutionLog(
        id="retry-success-execution",
        campaign_id=campaign.id,
        status="failed",
        attempt_count=1,
        retry_count=0,
        max_retries=3,
        error_message="previous publish failure",
        next_retry_at=datetime.utcnow() - timedelta(seconds=1),
        worker_name="campaign_scheduler",
    )
    db_session.add(execution)
    db_session.commit()

    class FakePublishService:
        @staticmethod
        def publish(db, campaign_id):
            return {
                "campaign_id": campaign_id,
                "status": "published",
                "results": [
                    {
                        "platform": "telegram",
                        "success": True,
                    }
                ],
            }

    import src.domains.campaign.services.scheduler_service as scheduler_service

    monkeypatch.setattr(
        scheduler_service,
        "CampaignPublishService",
        FakePublishService,
    )

    monkeypatch.setattr(
        scheduler_service,
        "SessionLocal",
        lambda: db_session,
    )

    monkeypatch.setattr(
        scheduler_service,
        "send_ceo_alert",
        lambda message: None,
    )

    process_retry_campaigns()

    execution_after = (
        db_session.query(CampaignExecutionLog)
        .filter(
            CampaignExecutionLog.id == execution.id,
        )
        .one()
    )

    assert execution_after.status == "success"
    assert execution_after.retry_count == 1
    assert execution_after.attempt_count == 2
    assert execution_after.next_retry_at is None
    assert execution_after.completed_at is not None
