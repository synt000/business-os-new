from dataclasses import dataclass


@dataclass
class IdentityContext:
    provider: str
    external_user_id: str
    external_chat_id: str | None = None
