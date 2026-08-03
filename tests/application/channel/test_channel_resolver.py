from src.application.channel.contracts import (
    ChannelResolutionRequest,
    ChannelResolutionResult,
)

from src.application.channel.resolver import (
    ChannelResolver,
)


def test_channel_resolution_request_contract():

    request = ChannelResolutionRequest(
        provider="telegram",
        external_channel_id="bot_001",
    )

    assert request.provider == "telegram"
    assert request.external_channel_id == "bot_001"
    assert request.verification_token is None


def test_channel_resolver_pending_result():

    request = ChannelResolutionRequest(
        provider="telegram",
        external_channel_id="bot_001",
    )

    result = ChannelResolver.resolve(
        db=None,
        request=request,
    )

    assert isinstance(
        result,
        ChannelResolutionResult,
    )

    assert result.resolved is False
    assert result.tenant_context is None
