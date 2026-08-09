from datetime import datetime, timedelta

from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.execution_models import CampaignExecutionLog
from src.domains.campaign.services.scheduler_service import process_retry_campaigns
from src.domains.social_center.models import SocialChannel


def test_campaign_retry_exhaustion_becomes_permanent_failure(
    db_session,
    tenant_id,
    monkeypatch,
):
    channel = SocialChannel(
        id="retry-permanent-channel",
        tenant_id=tenant_id,
        platform="telegram",
        channel_name="Permanent Failure Telegram",
        external_id="retry-permanent-chat-001",
        access_token="test-token",
        webhook_token="test-webhook",
        is_active=True,
    )
    db_session.add(channel)

    campaign = Campaign(
        id="retry-permanent-campaign",
        tenant_id=tenant_id,
        name="Permanent Failure Campaign",
        content="This will permanently fail",
        status="scheduled",
        is_active=True,
    )
    db_session.add(campaign)

    db_session.add(
        CampaignChannel(
            id="retry-permanent-campaign-channel",
            campaign_id=campaign.id,
            channel_id=channel.id,
        )
    )

    execution = CampaignExecutionLog(
        id="retry-permanent-execution",
        campaign_id=campaign.id,
        status="failed",
        attempt_count=3,
        retry_count=2,
        max_retries=3,
        error_message="previous failure",
        next_retry_at=datetime.utcnow() - timedelta(seconds=1),
        worker_name="campaign_scheduler",
    )
    db_session.add(execution)
    db_session.commit()

    campaign_id = campaign.id

    class FakePublishService:
        @staticmethod
        def publish(db, campaign_id):
            raise RuntimeError("simulated permanent failure")

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

    alerts = []

    monkeypatch.setattr(
        scheduler_service,
        "send_ceo_alert",
        lambda message: alerts.append(message),
    )

    process_retry_campaigns()

    execution_after = (
        db_session.query(CampaignExecutionLog)
        .filter(
            CampaignExecutionLog.id == execution.id,
        )
        .one()
    )

    assert execution_after.status == "failed_permanent"
    assert execution_after.retry_count == 3
    assert execution_after.attempt_count == 4
    assert execution_after.error_message == "simulated permanent failure"
    assert execution_after.next_retry_at is None
    assert len(alerts) == 1
    assert "Campaign Permanent Failure" in alerts[0]
    assert campaign_id in alerts[0]
