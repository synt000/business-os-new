import enum
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class SubscriptionTier(str, enum.Enum):
    FREE_TRIAL = "FREE_TRIAL"
    STARTUP = "STARTUP"
    ENTERPRISE = "ENTERPRISE"

class DeviceStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"

class Tenant(BaseModel):
    id: str = Field(..., description="Unique Tenant Identifier")
    company_name: str
    owner_email: str
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE_TRIAL
    trial_expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=3))
    is_billing_active: bool = True
    referral_code_used: Optional[str] = None
    accumulated_rewards_usd: float = 0.0

class DeviceNode(BaseModel):
    device_id: str
    device_name: str
    registered_ip: str
    status: DeviceStatus = DeviceStatus.ACTIVE
    last_login: datetime = Field(default_factory=datetime.utcnow)

class LicenseKeyRegistry(BaseModel):
    key_hash: str
    tenant_id: str
    max_devices_allowed: int = 5
    active_devices: List[DeviceNode] = []
    expires_at: datetime

class DynamicModulesRegistry(BaseModel):
    tenant_id: str
    enabled_modules: Dict[str, bool] = {
        "retail_pos": True, "restaurant_kms": False, "pharmacy_rx": False,
        "clinic_health": False, "hotel_pms": False, "ecom_aggregator": False,
        "logistics_fleet": False, "realestate_pms": False, "education_lms": False,
        "manufacturing_mrp": False, "salon_spa": False, "construction_pms": False,
        "garment_apparel": False, "microfinance_loan": False, "automotive_crm": False,
        "cargo_shipping": False, "jewelry_pos": False, "wholesale_distribution": False,
        "agriculture_agritech": False, "fitness_gym": False, "rental_car": False,
        "legal_case_management": False, "media_publishing": False, "travel_agency": False,
        "digital_agency_billing": False, "food_delivery_hook": False, "laundry_pos": False,
        "gas_station_meter": False
    }

class SocialIntegrationChannels(BaseModel):
    tenant_id: str
    facebook_page_token: Optional[str] = None
    telegram_bot_webhook: Optional[str] = None
    tiktok_shop_api_key: Optional[str] = None
    instagram_business_id: Optional[str] = None
    whatsapp_business_sid: Optional[str] = None
