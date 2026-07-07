from datetime import datetime, timezone
# Relative Package Import Layer (Bypassing ModuleNotFoundError)
from ..models.saas_core import Tenant, SubscriptionTier, LicenseKeyRegistry, DeviceNode, DeviceStatus

class SaaSPlatformOperationsEngine:
    """SaaS Engine For Trial Validity, Referral Rewards, and Dynamic Hardware Licensing Constraints."""
    
    def __init__(self):
        self.tenants_db = {}
        self.license_db = {}

    def verify_trial_access(self, tenant_id: str) -> dict:
        tenant: Tenant = self.tenants_db.get(tenant_id)
        if not tenant:
            return {"status": "ACCESS_DENIED", "reason": "TENANT_NOT_FOUND"}
            
        if tenant.subscription_tier == SubscriptionTier.FREE_TRIAL:
            if datetime.utcnow() > tenant.trial_expires_at:
                tenant.is_billing_active = False
                return {"status": "SUSPENDED", "reason": "3_DAY_TRIAL_EXPIRED_UPGRADE_REQUIRED"}
                
        return {"status": "ACTIVE", "tier": tenant.subscription_tier, "billing_state": tenant.is_billing_active}

    def process_referral_attribution(self, new_tenant_id: str, referrer_code: str) -> dict:
        referrer_tenant = None
        for t in self.tenants_db.values():
            if t.id == referrer_code:
                referrer_tenant = t
                break
                
        if referrer_tenant:
            referrer_tenant.accumulated_rewards_usd += 25.00
            return {"status": "CREDITED", "reward_usd": 25.00, "recipient_tenant": referrer_tenant.id}
            
        return {"status": "SKIPPED", "reason": "REFERRER_CODE_INVALID"}

    def authorize_device_session(self, license_key: str, hardware_uid: str, device_name: str, client_ip: str) -> dict:
        license_meta: LicenseKeyRegistry = self.license_db.get(license_key)
        if not license_meta:
            return {"status": "REJECTED", "reason": "LICENSE_KEY_NOT_FOUND"}
            
        if datetime.utcnow() > license_meta.expires_at:
            return {"status": "REJECTED", "reason": "EXPIRED_LICENSE_CONTRACT"}

        for current_device in license_meta.active_devices:
            if current_device.device_id == hardware_uid:
                if current_device.status == DeviceStatus.BLOCKED:
                    return {"status": "BLOCKED", "reason": "HARDWARE_SIGNATURE_SUSPENDED"}
                current_device.last_login = datetime.utcnow()
                return {"status": "AUTHORIZED", "device_context": "EXISTING_NODE"}

        if len(license_meta.active_devices) >= license_meta.max_devices_allowed:
            return {"status": "DENIED", "reason": "MAX_LICENSE_DEVICE_LIMIT_EXCEEDED"}

        new_node = DeviceNode(
            device_id=hardware_uid,
            device_name=device_name,
            registered_ip=client_ip
        )
        license_meta.active_devices.append(new_node)
        return {"status": "AUTHORIZED", "device_context": "NEW_NODE_REGISTERED"}
