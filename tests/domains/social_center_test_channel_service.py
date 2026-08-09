from src.domains.social_center.models import SocialChannel
from src.domains.social_center.schemas import SocialChannelCreate
from src.domains.social_center.service import SocialCenterService


def test_create_and_list_social_channel(db_session, tenant_id):
    data = SocialChannelCreate(
        platform="telegram",
        channel_name="Test Telegram",
        external_id="chat-test-001",
        access_token="test-token",
        webhook_token="test-webhook",
    )

    channel = SocialCenterService.create_channel(
        db_session,
        tenant_id,
        data,
    )

    assert channel.id is not None
    assert channel.tenant_id == tenant_id
    assert channel.platform == "telegram"
    assert channel.external_id == "chat-test-001"
    assert channel.is_active is True

    channels = SocialCenterService.list_channels(
        db_session,
        tenant_id,
    )

    assert len(channels) == 1
    assert channels[0].id == channel.id
