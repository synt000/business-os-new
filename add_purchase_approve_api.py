from pathlib import Path

p = Path("src/domains/purchase/router.py")
text = p.read_text(encoding="utf-8")

if "approve-ai-po" in text:
    print("Already exists")
    raise SystemExit

code = '''

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User, PurchaseOrder


@router.post("/approve-ai-po/{purchase_id}")
def approve_ai_purchase(
    purchase_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == purchase_id,
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not po:
        return {
            "status":"FAILED",
            "message":"Purchase Order Not Found"
        }

    po.status = "APPROVED"

    db.commit()

    return {
        "status":"SUCCESS",
        "message":"Purchase Order Approved",
        "purchase_number":po.purchase_number
    }

'''

p.write_text(text + code, encoding="utf-8")
print("Approve Purchase API Added")
