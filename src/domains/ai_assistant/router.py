from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from src.core.database import get_db

from src.core.security import get_current_user

from src.models.saas_core import User


from src.domains.ai_assistant.schemas import (
    AIChatRequest,
    AIChatResponse,
)


from src.domains.ai_assistant.service import (
    ask_ai,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)



@router.post(
    "/chat",
    response_model=AIChatResponse
)
def chat(
    data: AIChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    reply, category = ask_ai(
        db,
        current_user.tenant_id,
        data.message
    )


    return {
        "reply": reply,
        "category": category
    }
