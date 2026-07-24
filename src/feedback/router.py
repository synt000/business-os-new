from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.security import get_authenticated_user

from src.database import get_db

from .models import Feedback
from .schema import FeedbackCreate


router = APIRouter(
    prefix="/api/v4/feedback",
    tags=["Feedback"]
)



@router.post("")
def create_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):

    feedback = Feedback(

        tenant_id=current_user.tenant_id,

        user_id=str(current_user.id),

        feedback_type=data.feedback_type,

        subject=data.subject,

        message=data.message

    )


    db.add(feedback)

    db.commit()

    db.refresh(feedback)


    return {
        "status":"received",
        "message":"Thank you for your feedback"
    }
