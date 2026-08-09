from datetime import datetime, timedelta

from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.execution_models import CampaignExecutionLog
from src.domains.campaign.services.scheduler_service import process_scheduled_campaigns
from src.domains.social_center.models import SocialChannel


def test_scheduled_campaign_failure_creates_failed_execution(
    db_session,
    tenant_id,
    monkeypatch,
):
    channel = SocialChannel(
        id="scheduler-telegram-channel",
        tenant_id=tenant_id,
        platform="telegram",
        channel_name="Scheduler Telegram",
        external_id="scheduler-chat-001",
        access_token="test-token",
        webhook_token="test-webhook",
        is_active=True,
    )
    db_session.add(channel)

    campaign = Campaign(
        id="scheduler-failure-campaign",
        tenant_id=tenant_id,
        name="Scheduled Failure Campaign",
        content="Scheduled content",
        status="scheduled",
        scheduled_at=datetime.utcnow() - timedelta(minutes=1),
        is_active=True,
    )
    db_session.add(campaign)

    db_session.add(
        CampaignChannel(
            id="scheduler-campaign-channel",
            campaign_id=campaign.id,
            channel_id=channel.id,
        )
    )
    db_session.commit()

    class FakePublishService:
        @staticmethod
        def publish(db, campaign_id):
            raise RuntimeError("simulated publish failure")

    import src.domains.campaign.services.scheduler_service as scheduler_service

    monkeypatch.setattr(
        scheduler_service,
        "CampaignPublishService",
        FakePublishService,
    )

    import src.domains.campaign.services.scheduler_service as module

    monkeypatch.setattr(
        module,
        "SessionLocal",
        lambda: db_session,
    )

    monkeypatch.setattr(
        module,
        "send_ceo_alert",
        lambda message: None,
    )

    process_scheduled_campaigns()

    campaign_after = (
        db_session.query(Campaign)
        .filter(Campaign.id == campaign.id)
        .one()
    )
    assert campaign_after.status == "scheduled"


    execution = (
        db_session.query(CampaignExecutionLog)
        .filter(
            CampaignExecutionLog.campaign_id == campaign.id,
        )
        .one()
    )

    assert execution.status == "failed"
    assert execution.attempt_count == 1
    assert execution.error_message == "simulated publish failure"
    assert execution.completed_at is not None
