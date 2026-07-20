from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domains.website_settings.models import WebsiteSetting


router = APIRouter(
    prefix="/api/v1/website-settings",
    tags=["Website Settings"]
)


@router.get("/")
def get_settings(
    db: Session = Depends(get_db)
):

    settings = (
        db.query(WebsiteSetting)
        .first()
    )

    if not settings:
        settings = WebsiteSetting(
            live_message="🚀 Business OS Myanmar is currently in Pilot Testing Phase.",
            contact_email="sawyannaing054540@gmail.com",
            telegram="@Leekyitarlarkomaykoloe",
            phone="09686563395",
            viber="09686563395"
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


@router.post("/")
def create_settings(
    data: dict,
    db: Session = Depends(get_db)
):

    settings = WebsiteSetting(**data)

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return settings


@router.put("/")
def update_settings(
    data: dict,
    db: Session = Depends(get_db)
):

    settings = (
        db.query(WebsiteSetting)
        .first()
    )

    if not settings:
        settings = WebsiteSetting()

        db.add(settings)


    for key,value in data.items():
        if hasattr(settings,key):
            setattr(settings,key,value)


    db.commit()
    db.refresh(settings)

    return settings
