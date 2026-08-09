from pydantic import BaseModel
from datetime import datetime


class CampaignScheduleRequest(BaseModel):
    scheduled_at: datetime
