from sqlalchemy.orm import Session

from src.models.saas_core import (
    AIConversation,
)


def create_ai_message(
    db: Session,
    tenant_id: str,
    user_id: str,
    message: str,
):

    conversation = AIConversation(
        tenant_id=tenant_id,
        user_id=user_id,
        message=message,
        response="AI Assistant Ready",
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def ask_business_ai(
    message: str,
    business_type: str,
):

    if business_type == "ONLINE_SHOP":
        return (
            "Online Shop Assistant:\n"
            "- Order checking\n"
            "- Customer reply\n"
            "- Product suggestion\n"
            "- Sales report"
        )

    if business_type == "2D_SELLER":
        return (
            "2D Business Assistant:\n"
            "- Customer inquiry\n"
            "- Result notification\n"
            "- Daily operation support"
        )

    return (
        "Business AI Assistant:\n"
        "How can I help your business today?"
    )
