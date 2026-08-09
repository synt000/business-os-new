from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.services.publish_service import CampaignPublishService
from src.domains.social_center.models import SocialChannel
from src.domains.social_post.models import SocialPost
from src.domains.social_post.publish_log_models import SocialPublishLog


def test_campaign_publish_telegram_failure_creates_failed_publish_log(
    db_session,
    tenant_id,
    monkeypatch,
):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")

    channel = SocialChannel(
        id="telegram-channel-failure-test",
        tenant_id=tenant_id,
        platform="telegram",
        channel_name="Failure Telegram",
        external_id="chat-failure-001",
        access_token="test-token",
        webhook_token="test-webhook",
        is_active=True,
    )
    db_session.add(channel)

    campaign = Campaign(
        id="campaign-telegram-failure-test",
        tenant_id=tenant_id,
        name="Telegram Failure Campaign",
        content="This should fail",
        status="draft",
        is_active=True,
    )
    db_session.add(campaign)

    db_session.add(
        CampaignChannel(
            id="campaign-channel-failure-test",
            campaign_id=campaign.id,
            channel_id=channel.id,
        )
    )
    db_session.commit()

    class FakeResponse:
        ok = False
        text = '{"ok":false,"description":"test failure"}'

    def fake_post(url, json, timeout):
        return FakeResponse()

    import src.domains.social_post.adapters.telegram as telegram_adapter

    monkeypatch.setattr(telegram_adapter.requests, "post", fake_post)

    result = CampaignPublishService.publish(
        db_session,
        campaign.id,
    )

    assert result["status"] == "published"
    assert result["results"][0]["success"] is False

    post = (
        db_session.query(SocialPost)
        .filter(SocialPost.campaign_id == campaign.id)
        .one()
    )

    log = (
        db_session.query(SocialPublishLog)
        .filter(SocialPublishLog.post_id == post.id)
        .one()
    )

    assert log.platform == "telegram"
    assert log.success is False
    assert "test failure" in log.response

    db_session.refresh(campaign)
    assert campaign.status == "published"
