from src.domains.campaign.models import Campaign, CampaignChannel
from src.domains.campaign.services.publish_service import CampaignPublishService
from src.domains.social_center.models import SocialChannel
from src.domains.social_post.models import SocialPost
from src.domains.social_post.publish_log_models import SocialPublishLog


def test_campaign_publish_telegram_uses_channel_external_id(
    db_session,
    tenant_id,
    monkeypatch,
):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")

    channel = SocialChannel(
        id="telegram-channel-test",
        tenant_id=tenant_id,
        platform="telegram",
        channel_name="Test Telegram",
        external_id="chat-test-001",
        access_token="test-token",
        webhook_token="test-webhook",
        is_active=True,
    )
    db_session.add(channel)

    campaign = Campaign(
        id="campaign-telegram-test",
        tenant_id=tenant_id,
        name="Telegram Test Campaign",
        content="Hello Telegram",
        status="draft",
        is_active=True,
    )
    db_session.add(campaign)

    db_session.add(
        CampaignChannel(
            id="campaign-channel-test",
            campaign_id=campaign.id,
            channel_id=channel.id,
        )
    )
    db_session.commit()

    class FakeResponse:
        ok = True
        text = '{"ok":true}'

    captured = {}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    import src.domains.social_post.adapters.telegram as telegram_adapter

    monkeypatch.setattr(telegram_adapter.requests, "post", fake_post)

    result = CampaignPublishService.publish(
        db_session,
        campaign.id,
    )

    assert result["status"] == "published"
    assert result["results"][0]["success"] is True

    assert captured["json"]["chat_id"] == "chat-test-001"
    assert captured["json"]["text"] == "Hello Telegram"

    post = (
        db_session.query(SocialPost)
        .filter(SocialPost.campaign_id == campaign.id)
        .one()
    )
    assert post.channel_id == channel.id

    log = (
        db_session.query(SocialPublishLog)
        .filter(SocialPublishLog.post_id == post.id)
        .one()
    )
    assert log.platform == "telegram"
    assert log.success is True
