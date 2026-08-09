from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domains.social_post.schemas import (
    SocialPostCreate,
    SocialPostResponse,
)

from src.domains.social_post.services.publish_service import (
    SocialPostPublishService,
)


router = APIRouter(
    prefix="/social-posts",
    tags=["Social Posts"]
)


@router.post(
    "",
    response_model=SocialPostResponse
)
def create_social_post(
    payload: SocialPostCreate,
    db: Session = Depends(get_db)
):
    return SocialPostPublishService.create(
        db=db,
        payload=payload
    )


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[SocialPostResponse]
)
def list_social_posts(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    return SocialPostPublishService.list_by_tenant(
        db=db,
        tenant_id=tenant_id
    )


@router.post(
    "/{post_id}/publish",
    response_model=SocialPostResponse
)
def publish_social_post(
    post_id: str,
    db: Session = Depends(get_db)
):
    return SocialPostPublishService.publish(
        db=db,
        post_id=post_id
    )
