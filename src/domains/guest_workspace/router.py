from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import (
    GuestWorkspaceCreate,
    GuestWorkspaceResponse,
    GuestWorkspaceInfoResponse
)

from .service import GuestWorkspaceService


router = APIRouter(
    prefix="/guest",
    tags=["Guest Workspace"]
)


@router.post(
    "/workspace",
    response_model=GuestWorkspaceResponse
)
def create_guest_workspace(
    payload: GuestWorkspaceCreate,
    db: Session = Depends(get_db)
):

    workspace = GuestWorkspaceService.create_workspace(
        db=db,
        device_data=payload.device,
        guest_name=payload.guest_name,
        business_type_id=payload.business_type_id
    )

    return workspace



@router.get(
    "/workspace/{workspace_key}",
    response_model=GuestWorkspaceInfoResponse
)
def get_guest_workspace(
    workspace_key: str,
    db: Session = Depends(get_db)
):

    workspace = GuestWorkspaceService.get_workspace_info(
        db,
        workspace_key
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace
