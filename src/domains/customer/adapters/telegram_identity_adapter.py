from src.domains.customer.adapters.identity_adapter import IdentityAdapter
from src.domains.customer.contracts.identity_contract import IdentityContext


class TelegramIdentityAdapter(IdentityAdapter):
    """
    Telegram external identity translator.

    Responsibility:
    Telegram payload -> IdentityContext

    No database access.
    No service orchestration.
    """

    provider = "telegram"

    def resolve_identity(
        self,
        external_user_id: str,
        external_chat_id: str | None = None,
    ) -> IdentityContext:
        return IdentityContext(
            provider=self.provider,
            external_user_id=str(external_user_id),
            external_chat_id=(
                str(external_chat_id)
                if external_chat_id is not None
                else None
            ),
        )
