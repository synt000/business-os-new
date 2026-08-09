from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domains.campaign.models import Campaign
from src.domains.campaign.services.publish_service import CampaignPublishService
from src.domains.campaign.schemas import CampaignScheduleRequest
from src.domains.campaign.services.analytics_service import CampaignAnalyticsService


router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"]
)


@router.post("/{campaign_id}/publish")
def publish_campaign(
    campaign_id: str,
    db: Session = Depends(get_db)
):
    return CampaignPublishService.publish(
        db,
        campaign_id
    )


@router.get("/{campaign_id}/analytics")
def campaign_analytics(
    campaign_id: str,
    db: Session = Depends(get_db)
):
    return CampaignAnalyticsService.get_campaign_analytics(
        db,
        campaign_id
    )


@router.post("/{campaign_id}/schedule")
def schedule_campaign(
    campaign_id: str,
    payload: CampaignScheduleRequest,
    db: Session = Depends(get_db)
):
    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == campaign_id
        )
        .first()
    )

    if not campaign:
        return {
            "status": "NOT_FOUND",
            "message": "Campaign not found"
        }

    campaign.scheduled_at = payload.scheduled_at
    campaign.status = "scheduled"

    db.commit()
    db.refresh(campaign)

    return {
        "campaign_id": campaign.id,
        "status": campaign.status,
        "scheduled_at": campaign.scheduled_at
    }


@router.get("/{campaign_id}/executions")
def get_campaign_executions(campaign_id: str, db: Session = Depends(get_db)):
    from src.domains.campaign.execution_models import CampaignExecutionLog

    logs = (
        db.query(CampaignExecutionLog)
        .filter(
            CampaignExecutionLog.campaign_id == campaign_id
        )
        .order_by(
            CampaignExecutionLog.started_at.desc()
        )
        .all()
    )

    return [
        {
            "campaign_id": log.campaign_id,
            "status": log.status,
            "attempt_count": log.attempt_count,
            "worker_name": log.worker_name,
            "error_message": log.error_message,
            "started_at": log.started_at,
            "completed_at": log.completed_at,
        }
        for log in logs
    ]
