from pathlib import Path

p = Path("src/product/router.py")

s = p.read_text()

marker = '@router.put("/orders/{order_id}/payment")'

if '@router.get("/orders/{order_id}/invoice")' in s:
    print("ENDPOINT ALREADY EXISTS")
    raise SystemExit

endpoint = '''
@router.get("/orders/{order_id}/invoice")
async def get_order_invoice(
    order_id: str,
    current_user: User = Depends(require_active_subscription()),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.tenant_id == current_user.tenant_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")

    items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    return {
        "invoice_number": order.order_number,
        "customer": order.customer_name,
        "phone": order.customer_phone,
        "status": order.order_status,
        "total": order.total_amount,
        "items": [
            {
                "product_id": i.product_id,
                "qty": i.quantity,
                "price": i.price_at_sale,
                "subtotal": i.quantity * i.price_at_sale
            }
            for i in items
        ]
    }


'''

if marker not in s:
    raise SystemExit("PAYMENT ROUTE MARKER NOT FOUND")

s = s.replace(marker, endpoint + marker, 1)

p.write_text(s)

print("RESTORED GET /orders/{order_id}/invoice")
