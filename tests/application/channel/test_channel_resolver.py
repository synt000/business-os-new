from types import SimpleNamespace

from src.application.channel.contracts import (
    ChannelResolutionRequest,
    ChannelResolutionResult,
)

from src.application.channel.resolver import (
    ChannelResolver,
)


class MockQuery:

    def __init__(self, result):
        self.result = result

    def filter(self, *args):
        return self

    def first(self):
        return self.result


class MockDB:

    def __init__(self, result):
        self.result = result

    def query(self, model):
        return MockQuery(self.result)


def test_channel_resolution_request_contract():

    request = ChannelResolutionRequest(
        provider="telegram",
        external_channel_id="bot_001",
    )

    assert request.provider == "telegram"
    assert request.external_channel_id == "bot_001"
    assert request.verification_token is None


def test_channel_resolver_success():

    channel = SimpleNamespace(
        tenant_id="tenant_001",
        platform="telegram",
        external_id="bot_001",
        is_active=True,
    )

    db = MockDB(channel)

    request = ChannelResolutionRequest(
        provider="telegram",
        external_channel_id="bot_001",
    )

    result = ChannelResolver.resolve(
        db=db,
        request=request,
    )

    assert isinstance(
        result,
        ChannelResolutionResult,
    )

    assert result.resolved is True
    assert result.tenant_context.tenant_id == "tenant_001"


def test_channel_resolver_not_found():

    db = MockDB(None)

    request = ChannelResolutionRequest(
        provider="telegram",
        external_channel_id="missing",
    )

    result = ChannelResolver.resolve(
        db=db,
        request=request,
    )

    assert result.resolved is False
    assert result.tenant_context is None
