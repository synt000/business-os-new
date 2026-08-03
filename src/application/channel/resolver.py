from sqlalchemy.orm import Session

from src.application.channel.contracts import (
    ChannelResolutionRequest,
    ChannelResolutionResult,
)


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
        Resolve external channel to tenant context.

        Implementation intentionally pending.

        Phase 4.17:
        Contract boundary only.
        """

        return ChannelResolutionResult(
            resolved=False,
            message="Channel resolver implementation pending"
        )
