from pathlib import Path

p = Path("src/domains/purchase/router.py")
text = p.read_text(encoding="utf-8")

if '@router.get("/orders")' in text:
    print("Already exists")
    raise SystemExit

code = '''

from sqlalchemy import desc

from src.models.saas_core import PurchaseOrder


@router.get("/orders")
def list_purchase_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .order_by(desc(PurchaseOrder.created_at))
        .all()
    )

    return [
        {
            "id": r.id,
            "purchase_number": r.purchase_number,
            "status": r.status,
            "supplier_id": r.supplier_id,
            "total_amount": r.total_amount,
            "created_at": r.created_at
        }
        for r in rows
    ]

'''

p.write_text(text + code, encoding="utf-8")
print("Purchase List API Added")
