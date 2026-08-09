from src.domains.campaign.models import Campaign
from src.domains.campaign.services.publish_service import CampaignPublishService
from src.domains.social_post.models import SocialPost


def test_campaign_publish_without_channel_returns_no_channel(
    db_session,
    tenant_id,
):
    campaign = Campaign(
        id="campaign-no-channel-test",
        tenant_id=tenant_id,
        name="No Channel Campaign",
        content="This should not publish",
        status="draft",
        is_active=True,
    )
    db_session.add(campaign)
    db_session.commit()

    result = CampaignPublishService.publish(
        db_session,
        campaign.id,
    )

    assert result == {
        "status": "NO_CHANNEL",
        "message": "Campaign has no linked social channel",
    }

    posts = (
        db_session.query(SocialPost)
        .filter(SocialPost.campaign_id == campaign.id)
        .all()
    )

    assert posts == []
