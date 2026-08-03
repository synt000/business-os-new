from sqlalchemy.orm import Session

from src.application.channel.contracts import (
    ChannelResolutionRequest,
    ChannelResolutionResult,
)

from src.core.context.tenant_context import TenantContext
from src.domains.social_center.models import SocialChannel


class ChannelResolver:
    """
    Application channel resolution boundary.

    Responsibility:
    External Channel Identity
        ->
    Tenant Resolution Contract

    No customer logic.
    No identity logic.
    No business workflow.
    """

    @staticmethod
    def resolve(
        db: Session,
        request: ChannelResolutionRequest,
    ) -> ChannelResolutionResult:
        """
        Resolve external channel identity
        into tenant runtime context.

        Phase 4.18:
        SocialChannel lookup implementation.
        """

        channel = (
            db.query(SocialChannel)
            .filter(
                SocialChannel.platform == request.provider,
                SocialChannel.external_id == request.external_channel_id,
                SocialChannel.is_active == True,
            )
            .first()
        )

        if not channel:
            return ChannelResolutionResult(
                resolved=False,
                message="Channel not found"
            )

        tenant_context = TenantContext(
            tenant_id=channel.tenant_id
        )

        return ChannelResolutionResult(
            tenant_context=tenant_context,
            resolved=True,
            message="Channel resolved"
        )
