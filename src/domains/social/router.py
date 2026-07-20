from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.database_mega_upgrade import SocialWebhookLog
from src.models.saas_core import SocialMessage
from src.domains.inventory.models import Inventory
import json
import uuid

router = APIRouter(prefix="/social", tags=["Social Commerce Webhook"])

@router.post("/webhook/{tenant_id}")
async def handle_social_webhook(tenant_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Secure Webhook Ingress Endpoint to capture Facebook/TikTok incoming sales payload data
    and execute automated real-time inventory adjustments dynamically.
    """
    try:
        # 1. Parse raw incoming payload dynamically from social platform networks
        body_bytes = await request.body()
        payload_str = body_bytes.decode("utf-8")
        payload_json = json.loads(payload_str)
        
        # Determine platform context from header or fallback
        platform_source = request.headers.get("X-Platform-Source", "facebook")
        
        # 2. Persist transaction history log into upgraded mega schema
        webhook_entry = SocialWebhookLog(
            tenant_id=tenant_id,
            platform=platform_source,
            payload=payload_str,
            processed=False
        )
        db.add(webhook_entry)
        db.commit()
        db.refresh(webhook_entry)

        message_entry = SocialMessage(
            id=str(uuid.uuid4()),
            platform=platform_source.upper(),
            customer_name=payload_json.get("customer_name"),
            customer_id=payload_json.get("customer_id"),
            message=payload_json.get("message"),
            message_type="TEXT",
            status="NEW",
            tenant_id=tenant_id
        )

        db.add(message_entry)
        db.commit()
        
        # 3. Automated Inventory Deduction Simulation Engine if SKU matches inside payload
        # e.g. Expecting format: {"target_product_id": "uuid", "order_qty": 5}
        target_product = payload_json.get("target_product_id")
        order_qty = int(payload_json.get("order_qty", 0))
        
        if target_product and order_qty > 0:
            stock_record = db.query(Inventory).filter(
                Inventory.tenant_id == tenant_id,
                Inventory.product_id == target_product
            ).first()
            
            if stock_record:
                if stock_record.quantity >= order_qty:
                    stock_record.quantity -= order_qty # Execute automated inventory reduction
                    webhook_entry.processed = True
                    db.commit()
                    return {
                        "status": "success",
                        "message": "✓ Automation Engine: Order logged and Inventory deducted cleanly.",
                        "log_id": webhook_entry.id
                    }
                else:
                    return {"status": "partial", "message": "✗ Out of Stock context detected on live node.", "log_id": webhook_entry.id}
                    
        return {"status": "logged", "message": "Payload registered inside secure storage trail.", "log_id": webhook_entry.id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Webhook Engine Parse Fault: {e}")
