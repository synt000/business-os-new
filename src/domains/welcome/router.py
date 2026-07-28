from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import (
    WelcomeUpdate,
    WelcomeResponse
)

from .service import WelcomeService


router = APIRouter(
    prefix="/welcome",
    tags=["Welcome CMS"]
)


@router.get(
    "/{language}",
    response_model=WelcomeResponse
)
def get_welcome(
    language: str,
    db: Session = Depends(get_db)
):

    return WelcomeService.get_welcome(
        db,
        language
    )



@router.post(
    "/update",
    response_model=WelcomeResponse
)
def update_welcome(
    payload: WelcomeUpdate,
    db: Session = Depends(get_db)
):

    return WelcomeService.update_welcome(
        db,
        payload
    )
