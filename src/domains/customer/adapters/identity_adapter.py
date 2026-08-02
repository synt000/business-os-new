from abc import ABC, abstractmethod


class IdentityAdapter(ABC):
    """
    External identity provider adapter contract.
    Example providers:
    Telegram, Facebook, WhatsApp
    """

    provider: str = ""

    @abstractmethod
    def resolve_identity(
        self,
        external_user_id: str,
    ):
        pass
